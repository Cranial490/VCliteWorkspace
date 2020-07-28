from .models import *


def matching_engine(orderBook, order, parentOrder):
    if parentOrder.order_type == 'BUY' and orderBook.exists():
        # Buy order crossed the spread
        filled = 0
        consumed_asks = []
        for ask in orderBook:
            # if ask.user == order.user:
            #     continue
            if ask.ask_price > order.bid_price:
                break  # Price of ask is too high, stop filling order
            elif filled == order.quantity:
                break  # Order was filled

            if filled + ask.quantity <= order.quantity:  # order not yet filled, ask will be consumed whole
                filled += ask.quantity

                trade = Trade(bid=order,
                              ask=ask,
                              volume=-1,
                              parentOrder=parentOrder)

                consumed_asks.append(ask)

            elif filled + ask.quantity > order.quantity:  # order is filled, ask will be consumed partially
                volume = order.quantity - filled
                filled += volume

                trade = Trade(bid=order,
                              ask=ask,
                              volume=volume,
                              parentOrder=parentOrder)

                ask.quantity -= volume
                ask.save()
                # save the changes made here in ask
        # Place any remaining volume in LOB
        if filled < order.quantity:
            # self.orderbook.add(Order("limit", "buy", order.price, order.quantity-filled))
            order.quantity -= filled
            order.save()

        # Remove asks used for filling order
        for ask in consumed_asks:
            ask.delete()

    elif parentOrder.order_type == 'SELL' and orderBook.exists():
        # Sell order crossed the spread
        filled = 0
        consumed_bids = []
        for bid in orderBook:
            if bid.bid_price < order.ask_price:
                break  # Price of bid is too low, stop filling order
            elif filled == order.quantity:
                break  # Order was filled

            if filled + bid.quantity <= order.quantity:  # order not yet filled, bid will be consumed whole
                filled += bid.quantity
                trade = Trade(bid=bid,
                              ask=order,
                              volume=-1,
                              parentOrder=parentOrder)

                consumed_bids.append(bid)
            elif filled + bid.quantity > order.quantity:  # order is filled, bid will be consumed partially
                volume = order.quantity - filled
                filled += volume
                trade = Trade(bid=bid,
                              ask=order,
                              volume=volume,
                              parentOrder=parentOrder)

                bid.quantity -= volume
                bid.save()

        # Place any remaining volume in LOB
        if filled < order.quantity:
            order.quantity = order.quantity - filled
            order.save()

        # Remove bids used for filling order
        for bid in consumed_bids:
            bid.delete()

    else:
        order.save()
        # Order did not cross the spread, place in order book
        # self.orderbook.add(order)

# created a trade and adds in order queue


def Trade(bid, ask, volume, parentOrder):
    if parentOrder.order_type == 'BUY':
        if volume > 0:
            childBid = VC_T_Order_Executed(
                parent_order=parentOrder,
                price=bid.bid_price,
                filled_quantity=volume)

            childAsk = VC_T_Order_Executed(
                parent_order=ask.parent_order,
                price=ask.ask_price,
                filled_quantity=volume)

            parentOrder.updated_quantity = parentOrder.updated_quantity - volume
            if(parentOrder.updated_quantity == 0):
                parentOrder.order_status = "EXECUTED"
            parentOrder.save()
            childBid.save()
            childAsk.save()

            queueEntry = OrderQ(buyer=bid.user,
                                seller=ask.user,
                                parentOrder=parentOrder,
                                buyer_order_child=childBid,
                                seller_order_child=childAsk,
                                price=bid.bid_price,
                                quantity=volume)

        else:
            childBid = VC_T_Order_Executed(
                parent_order=parentOrder,
                price=bid.bid_price,
                filled_quantity=ask.quantity)

            childAsk = VC_T_Order_Executed(
                parent_order=ask.parent_order,
                price=ask.ask_price,
                filled_quantity=ask.quantity)

            parentOrder.updated_quantity -= ask.quantity
            if(parentOrder.updated_quantity == 0):
                parentOrder.order_status = "EXECUTED"
            parentOrder.save()
            ask.parent_order.updated_quantity -= ask.quantity
            if(ask.parent_order.updated_quantity == 0):
                ask.parent_order.order_status = "EXECUTED"
            ask.parent_order.save()
            childBid.save()
            childAsk.save()

            queueEntry = OrderQ(buyer=bid.user,
                                seller=ask.user,
                                buyer_order_child=childBid,
                                seller_order_child=childAsk,
                                price=bid.bid_price,
                                quantity=ask.quantity)

    elif parentOrder.order_type == 'SELL':
        if volume > 0:
            childBid = VC_T_Order_Executed(
                parent_order=bid.parent_order,
                price=bid.bid_price,
                filled_quantity=volume)

            childAsk = VC_T_Order_Executed(
                parent_order=parentOrder,
                price=ask.ask_price,
                filled_quantity=volume)

            parentOrder.updated_quantity = parentOrder.updated_quantity - volume
            if(parentOrder.updated_quantity == 0):
                parentOrder.order_status = "EXECUTED"

            parentOrder.save()

            bid.parent_order.updated_quantity -= bid.quantity
            bid.parent_order.save()
            childBid.save()
            childAsk.save()

            queueEntry = VC_T_Order_Queue(buyer=bid.user,
                                          seller=ask.user,
                                          buyer_order_child=childBid,
                                          seller_order_child=childAsk,
                                          price=ask.ask_price,
                                          quantity=volume)
        else:
            childBid = VC_T_Order_Executed(
                parent_order=bid.parent_order,
                price=bid.bid_price,
                filled_quantity=bid.quantity)

            childAsk = VC_T_Order_Executed(
                parent_order=parentOrder,
                price=ask.ask_price,
                filled_quantity=bid.quantity)

            parentOrder.updated_quantity -= bid.quantity
            if(parentOrder.updated_quantity == 0):
                parentOrder.order_status = "EXECUTED"
            parentOrder.save()

            bid.parent_order.updated_quantity -= bid.quantity
            if(bid.parent_order.updated_quantity == 0):
                bid.parent_order.order_status = "EXECUTED"
            bid.parent_order.save()
            childBid.save()
            childAsk.save()

            queueEntry = OrderQ(buyer=bid.user,
                                seller=ask.user,
                                buyer_order_child=childBid,
                                seller_order_child=childAsk,
                                price=ask.ask_price,
                                quantity=bid.quantity)

    queueEntry.save()
    return queueEntry
