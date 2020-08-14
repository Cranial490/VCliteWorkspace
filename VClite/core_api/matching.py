from .models import *


def matching_engine(orderBook, orderType, order):
    print(orderBook)
    print(order)
    print(orderType)
    parentOrder = orderHistoryCreate(order, orderType)
    if orderType == 'buy' and orderBook.exists():
        # Buy order crossed the spread
        filled = 0
        consumed_asks = []
        tradebook = []
        for ask in orderBook:
            if ask.ask_price > order.bid_price:
                break  # Price of ask is too high, stop filling order
            elif filled == order.quantity:
                break  # Order was filled

            if filled + ask.quantity <= order.quantity:  # order not yet filled, ask will be consumed whole
                filled += ask.quantity
                trade = Trade(bid=order, ask=ask, volume=-1,
                              parentOrder=parentOrder, orderType=orderType)
                tradebook.append(trade)
                consumed_asks.append(ask)
            elif filled + ask.quantity > order.quantity:  # order is filled, ask will be consumed partially
                volume = order.quantity - filled
                filled += volume
                trade = Trade(bid=order, ask=ask, volume=volume,
                              parentOrder=parentOrder, orderType=orderType)
                tradebook.append(trade)
                ask.quantity -= volume
                ask.save()
                # save the changes made here in ask
        # Place any remaining volume in LOB
        if filled < order.quantity:
            # self.orderbook.add(Order("limit", "buy", order.price, order.quantity-filled))
            order.quantity = order.quantity - filled
            createBid(order)  # TODO if we do this we will have 2 orders at 1 point of time (Rs.20,10) and (Rs.20,4)
            print("add remaining order to table" +
                  str(order.quantity - filled)) # TODO -> problem here -> should be str(order.quantity)

        # Remove asks used for filling order
        for ask in consumed_asks:
            ask.delete() #TODO update bids order, coz if we create bid order timestamp will be latest
            print("Delete consumed orders from table" + str(ask.quantity))
        return consumed_asks
    elif orderType == 'sell' and orderBook.exists():
        # Sell order crossed the spread
        filled = 0
        consumed_bids = []
        tradebook = []
        for bid in orderBook:
            if bid.bid_price < order.ask_price:
                break  # Price of bid is too low, stop filling order
            elif filled == order.quantity:
                break  # Order was filled

            if filled + bid.quantity <= order.quantity:  # order not yet filled, bid will be consumed whole
                filled += bid.quantity
                trade = Trade(bid=bid, ask=order, volume=-1,
                              parentOrder=parentOrder, orderType=orderType)
                tradebook.append(trade)
                consumed_bids.append(bid)
            elif filled + bid.quantity > order.quantity:  # order is filled, bid will be consumed partially
                volume = order.quantity - filled
                filled += volume
                trade = Trade(bid=bid, ask=order, volume=volume,
                              parentOrder=parentOrder, orderType=order)
                tradebook.append(trade)
                bid.quantity -= volume
                bid.save()
        # Place any remaining volume in LOB
        if filled < order.quantity:
            self.orderbook.add(
                Order("limit", "sell", order.price, order.quantity - filled))
            print("add remaining order to table" +
                  str(order.quantity - filled))

        # Remove bids used for filling order
        for bid in consumed_bids:
            bid.delete()
            print("Delete consumed orders from table" + str(bid.quantity))
        return consumed_bids
    else:
        if orderType == 'buy':
            createBid(order)
        elif orderType == 'sell':
            createAsk(order)
        # Order did not cross the spread, place in order book
        # self.orderbook.add(order)

# created a trade and adds in order queue


def Trade(bid, ask, volume, parentOrder, orderType):
    # trade = OrderQ(buyer_id=)
    if orderType == 'buy':
        if volume > 0:
            qEntry = OrderQ(buyer=bid.user, seller=ask.user,
                            price=bid.bid_price, quantity=volume, order=parentOrder)
        else:
            qEntry = OrderQ(buyer=bid.user, seller=ask.user,
                            price=bid.bid_price, quantity=ask.quantity, order=parentOrder)
    elif orderType == 'sell':
        if volume > 0:
            qEntry = OrderQ(buyer=bid.user, seller=ask.user,
                            price=bid.bid_price, quantity=volume, order=parentOrder)
        else:
            qEntry = OrderQ(buyer=bid.user, seller=ask.user,
                            price=bid.bid_price, quantity=bid.quantity, order=parentOrder)
    qEntry.save()
    return qEntry

def createAsk(order):
    ask = Ask(user=order.user, share=order.share,
              ask_price=order.ask_price, quantity=order.quantity)
    ask.save()


def createBid(order):
    bid = Bid(user=order.user, share=order.share,
              bid_price=order.bid_price, quantity=order.quantity)
    bid.save()


def orderHistoryCreate(order, orderType):
    if orderType == 'buy':
        newOrder = Order(user=order.user, share=order.share,
                         price=order.bid_price, quantity=order.quantity)
    elif orderType == 'sell':
        newOrder = Order(user=order.user, share=order.share,
                         price=order.ask_price, quantity=order.quantity)
    newOrder.save()
    return newOrder
