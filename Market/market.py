import grpc
import numpy as np
from concurrent import futures
import market_pb2
import market_pb2_grpc


class MarketService(market_pb2_grpc.MarketServiceServicer):
    def __init__(self):
        self.seller_registry = {}
        self.items_for_sale = {}
        self.buyer_wishlists = {}
        self.buyer_ratings = {}


    def RegisterSeller(self, request, context):
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid
        print(f"Seller join request from {seller_address}, uuid = {seller_uuid}")

        if seller_address in self.seller_registry:
            return market_pb2.SellerResponse(status = "FAIL")
        else:
            self.seller_registry[seller_address] = seller_uuid.replace(" ", "")

            return market_pb2.SellerResponse(status = "SUCCESS")


    def SellItem(self, request, context):
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid
        print(f"Sell Item request from {seller_address}")

        if seller_address in self.seller_registry and seller_uuid == self.seller_registry[seller_address]:
            item_id = len(self.items_for_sale) + 1

            self.items_for_sale[item_id] = market_pb2.Item(
                seller_info = market_pb2.SellerInfo(
                    address = seller_address,
                    uuid = seller_uuid
                ),
                id = str(item_id),
                name = request.product_name,
                category = request.category,
                description = request.description,
                price = request.price_per_unit,
                quantity = request.quantity,
                rating = 0
            )

            return market_pb2.SellItemResponse(status = "SUCCESS")
        else:
            return market_pb2.SellItemResponse(status = "FAIL")


    def UpdateItem(self, request, context):
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid
        item_id = int(request.item_id)
        new_price = request.new_price
        new_quantity = request.new_quantity
        print(f"Update Item {item_id} request from {seller_address}")

        if seller_address in self.seller_registry and self.seller_registry[seller_address] == seller_uuid:
            if item_id in self.items_for_sale:
                item_details = self.items_for_sale[item_id]
                item_details.price = new_price
                item_details.quantity = new_quantity            
                    
                return market_pb2.UpdateItemResponse(status = "SUCCESS")
            else:
                return market_pb2.UpdateItemResponse(status = "FAIL")
        else:
            return market_pb2.UpdateItemResponse(status = "FAIL")


    def DeleteItem(self, request, context):
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid
        item_id = int(request.id)
        print(f"Delete Item {item_id} request from {seller_address}")

        if seller_address in self.seller_registry and self.seller_registry[seller_address] == seller_uuid:
            if item_id in self.items_for_sale:
                del self.items_for_sale[item_id]

                return market_pb2.DeleteItemResponse(status = "SUCCESS")
            else:
                return market_pb2.DeleteItemResponse(status = "FAIL")
        else:
            return market_pb2.DeleteItemResponse(status = "FAIL")


    def DisplaySellerItems(self, request, context):
        seller_address = request.seller_info.address
        seller_uuid = request.seller_info.uuid
        print(f"Display Items request from {seller_address}")

        if seller_address in self.seller_registry and self.seller_registry[seller_address] == seller_uuid:
            items_response = ""

            for item_id, item_details in self.items_for_sale.items():
                items_response += f"\n{self.format_item_details(item_details)}"

            return market_pb2.DisplaySellerItemsResponse(items = items_response)
        else:
            return market_pb2.DisplaySellerItemsResponse(items = "FAIL")
    
    
    def SearchItem(self, request, context):
        item_name = request.name
        item_category = request.category
        print(f"Search request for Item name: {item_name}, Category: {item_category}.")
        matching_items_response = ""

        for id, item in self.items_for_sale.items():
            if (item_name.lower() in item.name.lower()) and (item_category == "ANY" or item.category == item_category):
                matching_items_response += f"\n{self.format_item_details(item)}"
        
        return market_pb2.SearchItemResponse(items = matching_items_response)

    
    def BuyItem(self, request, context):
        buyer_address = request.address
        item_id = int(request.id)
        quantity_to_purchase = request.quantity
        print(f"Buy request {quantity_to_purchase} of item {item_id} from {buyer_address}")
        
        if item_id in self.items_for_sale:
            item_details = self.items_for_sale[item_id]

            if item_details.quantity >= quantity_to_purchase:
                item_details.quantity -= quantity_to_purchase
                seller_info = item_details.seller_info
                # self.NotifyClient(seller_info, item_id)

                return market_pb2.BuyItemResponse(status = "SUCCESS")
            else:
                return market_pb2.BuyItemResponse(status = "FAIL")
        else:
            return market_pb2.BuyItemResponse(status = "FAIL")
    
    
    def AddToWishList(self, request, context):
        buyer_address = request.address
        item_id = request.id
        print(f"Wishlist request of item {item_id}, from {buyer_address}")

        try:
            if buyer_address not in self.buyer_wishlists:
                self.buyer_wishlists[buyer_address] = []

            self.buyer_wishlists[buyer_address].append(item_id)

            return market_pb2.WishlistResponse(status = "SUCCESS")
        except Exception as e:
            return market_pb2.WishlistResponse(status = "FAIL")

    
    def RateItem(self, request, context):
        buyer_address = request.address
        uuid = request.uuid
        item_id = request.id
        rating = request.rating

        try:
            if (item_id, uuid) in self.buyer_ratings:
                return market_pb2.RateItemResponse(status = "FAIL")
            
            if 0 <= rating <= 5:
                self.buyer_ratings[item_id] = []
                temp = market_pb2.RateItem(
                    item_id = item_id,
                    uuid = uuid,
                    rating = rating,
                    address = buyer_address
                )
                
                self.buyer_ratings[item_id].append(temp)
                rating = 0
                
                for rate in self.buyer_ratings[item_id]:
                    rating += rate.rating
                
                for id, item in self.items_for_sale.items():
                    if id == item_id:
                        item.rating = rating
                
                print(f"{buyer_address} rated item {item_id} with {rating} stars.")

                return market_pb2.RateItemResponse(status = "SUCCESS")
            else:
                return market_pb2.RateItemResponse(status = "FAIL")
        except Exception as e:
            return market_pb2.RateItemResponse(status = "FAIL")
    
    
    def NotifyClient(self, client_info, item_id):
        item_details = self.items_for_sale.get(item_id)

        if item_details:
            notification_message = f"""
            #######
            The Following Item has been Updated:

            Item ID: {item_id}, Price: ${item_details.pricePerUnit}, Name: {item_details.productName}, Category: {item_details.category},
            Description: {item_details.description},
            Quantity Remaining: {item_details.quantity}
            Rating: {item_details.rating} / 5  |  Seller: {item_details.sellerAddress}
            #######
            """
    
    
    def format_item_details(self, item):
        return (
            f"Item ID: {item.id}\n"
            f"Price: ${item.price}\n"
            f"Name: {item.name}\n"
            f"Category: {item.category}\n"
            f"Description: {item.description}\n"
            f"Quantity Remaining: {item.quantity}\n"
            f"Rating: {item.rating} / 5"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServiceServicer_to_server(MarketService(), server)
    server.add_insecure_port('[::]:5100')
    server.start()
    print("Market server started...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
