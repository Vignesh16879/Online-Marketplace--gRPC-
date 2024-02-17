import grpc
import uuid
import socket
import market_pb2
import market_pb2_grpc


class MarketClient:
    def __init__(self, market_address="localhost:5100"):
        self.buyer_address = get_ip()
        self.market_address = market_address
        self.uuid = str(uuid.uuid1())
        self.channel = grpc.insecure_channel(self.market_address)
        self.stub = market_pb2_grpc.MarketServiceStub(self.channel)


    def search_item(self, item_name = "", category = "ANY"):
        request = market_pb2.SearchItemRequest(
            name = item_name,
            category = category
        )

        try:
            response = self.stub.SearchItem(request)
            print(f"{response.items}")
        except grpc.RpcError as e:
            print("FAIL")


    def buy_item(self, item_id, quantity_to_purchase):
        request = market_pb2.BuyItemRequest(
            uuid = self.uuid,
            id = item_id,
            quantity = quantity_to_purchase,
            address = self.buyer_address
        )

        try:
            response = self.stub.BuyItem(request)
            print(f"{response.status}")
        except grpc.RpcError as e:
            print("FAIL")


    def add_to_wishlist(self, item_id):
        request = market_pb2.WishlistRequest(            
            uuid = self.uuid,
            id = item_id,
            address = self.buyer_address
        )

        try:
            response = self.stub.AddToWishList(request)
            print(f"{response.status}")
        except grpc.RpcError as e:
            print("FAIL")
        

    def rate_item(self, item_id, rating):
        request = market_pb2.RateItemRequest(
            uuid = self.uuid,
            id = item_id,
            rating = rating,
            address = self.buyer_address
        )

        try:
            response = self.stub.RateItem(request)
            print(f"{response.status}")
        except grpc.RpcError as e:
            print("FAIL")


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        
        return ip_address
    except Exception as e:
        return "127.0.0.1"


def ClientService():
    market_client = MarketClient()
    
    while True:
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add Item to WishList")
        print("4. Rate Item")
        print("5. Exit")
        inp = int(input("Choose Option: "))
        
        if inp == 1:
            name = input("Name: ")
            category = input("Category: ")
            if len (category) > 0:
                market_client.search_item(name, category)
            else:
                market_client.search_item(name)
        elif inp == 2:
            id = input("Item ID to buy: ")
            quantity = int(input("Quantity to purchase: "))
            market_client.buy_item(id, quantity)
        elif inp == 3:
            id = input("Item ID to add to WishList: ")
            market_client.add_to_wishlist(id)
        elif inp == 4:
            id = input("Item ID to rate: ")
            rate = int(input("Rating(0 - 5): "))
            market_client.rate_item(id, rate)
        elif inp == 5:
            break
        else:
            pass            


if __name__ == "__main__":
    ClientService()