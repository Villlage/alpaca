class DCA3C(bt.Strategy):
    params = (
        ('tp', 1.25),  # % above average buy price to sell at
        ('bo', 10),  # $ used for 1st buy
        ('so', 20),  # $ used for 2nd
        ('mstc', 30),  # Number of orders to keep filling while waiting for bounce to TP
        ('os', 1.05),  # Volume Scale
        ('sos', 2),  # Price Deviation To Open Safety Order
        ('ss', 1),  # Step Scale
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime()
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Update TP to include making back the commission
        self.params.tp += commission
        # Keep a reference to the "close" line in the data[0] dataseries
        self.price = self.datas[0].close
        # Store the sell order (take profit) so we can cancel and update tp price with ever filled SO
        self.tp_order = None
        # Store all the Safety Orders so we can cancel the unfilled ones after TPing
        self.orders = []

        # Current deal variables for managing safety orders
        # Cannot use self.getposition(self.data) as it only updates after candle close
        # and will not reflect candles where multiple SOs need to be placed
        self.deal_sum_avg_buy_price, self.deal_sum_size, self.deal_avg_entry_price = 0, 0, 0

    def notify_order(self, order):
        # Debugging
        # if order.status in [order.Submitted, order.Accepted]:
        #     if order.isbuy():
        #         print('BUY SUBMITTED ' + str(order.status))
        #     else:
        #         print('SELL SUBMITTED ' + str(order.status))
        #     # Buy/Sell order submitted/accepted to/by broker - Nothing to do
        #     # return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:

            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Size: %.5f Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.size, order.executed.price, order.executed.value, order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

                # Update current deal variables
                self.deal_sum_avg_buy_price += order.executed.size / order.executed.price
                self.deal_sum_size += order.executed.size
                self.deal_avg_entry_price = self.deal_sum_size / self.deal_sum_avg_buy_price

                # Update the sell order take profit price every time a new safety order is filled
                self.set_tp()

            else:  # Sell
                # Debugging
                print(
                    f'DEBUGGING: Size {self.deal_sum_size} Take Profit Price {self.deal_avg_entry_price * (1 + (self.params.tp / 100))}')

                self.log('SELL EXECUTED, Size: %.5f Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.size, order.executed.price, order.executed.value, order.executed.comm))

                # Cancel all of the unfilled safety orders
                [self.cancel(order) for order in self.orders]
                # Clear the list to store orders for the next deal
                self.orders = []
                # Clear variable to store new sell order (TP)
                self.tp_order = None
                # Clear out current deal variables
                self.deal_sum_avg_buy_price, self.deal_sum_size, self.deal_avg_entry_price = 0, 0, 0

        # Debugging
        # elif order.status in [order.Canceled, order.Margin, order.Rejected]:
        elif order.status in [order.Margin]:
            self.log('Order Margin')

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f, Size: %.5f' %
                 (trade.pnl, trade.pnlcomm, trade.size))
        print(self.position)

    def set_tp(self):
        '''
        Function to update the take profit order when new safety orders are placed
        :return:
        '''
        # If a sell order has already been made, cancel it
        if self.tp_order is not None:
            self.cancel(self.tp_order)
        # Create the new take profit sell order
        self.tp_order = self.sell(price=self.deal_avg_entry_price * (1 + (self.params.tp / 100)),
                                  exectype=bt.Order.Limit, size=self.deal_sum_size)

    def next(self):
        # If we are not in the market start the next deal
        if self.deal_sum_size == 0:
            print('')
            print('*** NEW DEAL ***')
            # print(self.position)
            # Place the initial BO (market)
            # Want to only buy as much as the $ amount of self.bo, so divide by price to get volume (size)
            self.orders.append(
                self.buy(
                    size=self.params.bo / self.price[0],
                    price=self.price[0])
            )
            # Set initial TP
            self.tp_order = self.sell(price=self.price[0] * (1 + (self.params.tp / 100)),
                                      size=self.params.bo / self.price[0],
                                      exectype=bt.Order.Limit)

            # Place the first SO (limit)
            so_price = self.price[0] * ((100 - (self.params.sos * self.params.ss)) / 100)
            self.orders.append(
                self.buy(price=so_price,
                         size=self.params.so / so_price,
                         exectype=bt.Order.Limit,
                         )
            )
            # Set all Safety Orders
            sos = self.params.sos
            for so_num in range(2, self.params.mstc + 1):
                so_limit_price = self.orders[-1].params.price * ((100 - sos) / 100)
                so_size = self.orders[-1].params.size * self.params.os
                self.orders.append(
                    self.buy(price=so_limit_price,
                             size=so_size,
                             exectype=bt.Order.Limit,
                             )
                )
                sos *= self.params.ss
