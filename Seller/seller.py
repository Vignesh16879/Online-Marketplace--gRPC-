import grpc
import uuid
import socket
import market_pb2
import market_pb2_grpc


class SellerClient:
    def __init__(self, market_address = "localhost:5100"):
        self.seller_address = get_ip()
        self.seller_uuid = str(uuid.uuid1())
        self.market_address = market_address
        self.channel = grpc.insecure_channel(self.market_address)
        self.stub = market_pb2_grpc.MarketServiceStub(self.channel)


    def register_seller(self):
        request = market_pb2.SellerRequest(
            seller_info = market_pb2.SellerInfo(
                address = self.seller_address,
                uuid = self.seller_uuid
            )
        )

        try:
            response = self.stub.RegisterSeller(request)
            print(f"{response.status}")
        except grpc.RpcError as e:
            print("FAIL")


    def sell_item(self, item_details):
        request = market_pb2.SellItemRequest(
            seller_info = market_pb2.SellerInfo(
                address = self.seller_address,
                uuid = self.seller_uuid
            ),
            product_name = item_details['name'],
            category = item_details['category'],
            quantity = item_details['quantity'],
            description = item_details['description'],
            price_per_unit = item_details['price']
        )

        try:
            response = self.stub.SellItem(request)
            print(f"{response.status}")
        except grpc.RpcError as e:
            print("FAIL")

    
    def update_item(self, id, new_price, new_quantity):
        request = market_pb2.UpdateItemRequest(
            seller_info = market_pb2.SellerInfo(
                address = self.seller_address,
                uuid = self.seller_uuid
            ),
            item_id = id,
            new_price = new_price,
            new_quantity = new_quantity
        )

        try:
            response = self.stub.UpdateItem(request)
            print(f"{response.status}")
        except grpc.RpcError as e:
            print(e)
            print("FAIL")
    
    
    def DisplaySellerItems(self):
        request = market_pb2.DisplaySellerItemsRequest(
            seller_info = market_pb2.SellerInfo(
                address = self.seller_address,
                uuid = self.seller_uuid
            )
        )
        
        try:
            response = self.stub.DisplaySellerItems(request)
            print(f"{response.items}")
        except grpc.RpcError as e:
            print("FAIL")


    def delete_item(self, item_id):
        request = market_pb2.DeleteItemRequest(
            seller_info = market_pb2.SellerInfo(
                address = self.seller_address,
                uuid = self.seller_uuid
            ),
            id = item_id
        )

        try:
            response = self.stub.DeleteItem(request)
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
    

def SellerService():
    seller_client = SellerClient()
    
    while True:
        print("1. Register")
        print("2. Sell Item")
        print("3. Update Item")
        print("4. Display All Items")
        print("5. Delete Item")
        print("6. Exit")
        inp = int(input("Choose Option: "))
        
        if inp == 1:
            seller_client.register_seller()
        elif inp == 2:
            name = input("Product name: ")
            category = input("Product category: ")
            quantity = int(input("Product quantity: "))
            description = input("Product description: ")
            price = float(input("Product price: "))
            item_details = {
                "name" : name,
                "category" : category,
                "quantity" : quantity,
                "description" : description,
                "price" : price
            }
            seller_client.sell_item(item_details)
        elif inp == 3:
            id = str(input("Product ID: "))
            price = float(input("Product New Price: "))
            quantity = int(input("Product New Quantity: "))
            seller_client.update_item(id, price, quantity)
        elif inp == 4:
            seller_client.DisplaySellerItems()
        elif inp == 5:
            id = input("Product ID to delete: ")
            seller_client.delete_item(id)
        elif inp == 6:
            break
        else:
            pass 


if __name__ == "__main__":
    SellerService()