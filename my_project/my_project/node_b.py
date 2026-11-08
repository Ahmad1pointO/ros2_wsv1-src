# # # # # import rclpy
# # # # # from rclpy.node import Node
# # # # # from std_msgs.msg import String

# # # # # class NodeB(Node):
# # # # #     def __init__(self):
# # # # #         super().__init__('node_b')
# # # # #         # Create a subscriber that listens to String messages on the '/status' topic
# # # # #         self.subscription = self.create_subscription(
# # # # #             String,
# # # # #             'status',
# # # # #             self.listener_callback,
# # # # #             10)
# # # # #         self.get_logger().info('Node B (Subscriber) has started!')

# # # # #     def listener_callback(self, msg):
# # # # #         # This function runs automatically whenever a new message arrives
# # # # #         self.get_logger().info(f'I heard: "{msg.data}"')

# # # # # def main(args=None):
# # # # #     rclpy.init(args=args)
# # # # #     node = NodeB()
# # # # #     rclpy.spin(node)
# # # # #     rclpy.shutdown()

# # # # # if __name__ == '__main__':
# # # # #     main()


# # # # """ making the Subscriber of a Topic to fetch the String data from the Publisher """
# # # # import  rclpy
# # # # from std_msgs.msg import String

# # # # def listener_callback(msg, node):
# # # #     node.get_logger().info(f'I heard: "{msg.data}"')

# # # # def main(args = None):
# # # #     rclpy.init(args=args)
# # # #     node = rclpy.create_node('node_b')
# # # #     node.create_subscription(String, 'status', lambda x: listener_callback(x, node), 10)
# # # #     node.get_logger().info('Node B (Functional Subscriber) has started!')

# # # #     rclpy.spin(node)
# # # #     rclpy.shutdown()

# # # # if __name__ == '__main__':
# # # #     main()


# # # """ Making a Subscriber that fetch the int data from a Topic published by Publisher on that topic"""
# # # import rclpy
# # # from std_msgs.msg import Int32

# # # def listener_callback(msg, node):
# # #     node.get_logger().info(f'I heared: {msg.data}')
# # #     # if msg.data >=9:
# # #     #     node.get_logger().info('Heard 9! from the Publisher, and now stoping the subscriber')
# # #     #     node.destroy_node()
# # #     #     rclpy.shutdown()


# # # def main(args = None):
# # #     rclpy.init(args=args)
# # #     node = rclpy.create_node('node_b')
# # #     node.create_subscription(Int32, 'Data', lambda x:listener_callback(x, node), 10)
# # #     node.get_logger().info('Node B (Funcrional Listener) has started')

# # #     try:
# # #         rclpy.spin(node)
# # #     except(KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # #         pass

# # # if __name__ == '__main__':
# # #     main()
    


# # # """Implementing the Service 
# # # /ping_worker: Node A calls this service, and Node B hosts the server.
# # # /ping_coordinator: Node B calls this service, and Node A hosts the server.
# # # # """
# # # import rclpy
# # # from example_interfaces.srv import Trigger

# # # # --- 1. THE SERVICE SERVER LOGIC (Node B receives a request and replies) ---
# # # def worker_service_callback(request, response):
# # #     # This runs when Node A calls '/ping_worker'
# # #     response.success = True
# # #     response.message = "Pong from Worker!"
# # #     return response

# # # # --- 2. THE SERVICE CLIENT LOGIC (Node B asks Node A for data) ---
# # # def call_coordinator_service(node, client):
# # #     while not client.wait_for_service(timeout_sec=1.0):
# # #         node.get_logger().info('Waiting for coordinator service to become available...')
        
# # #     req = Trigger.Request()
    
# # #     node.get_logger().info('Sending Request to Coordinator: "Ping"')
# # #     future = client.call_async(req)
    
# # #     def response_received_callback(completed_future):
# # #         try:
# # #             result = completed_future.result()
# # #             node.get_logger().info(f'Received Response from Coordinator: "{result.message}"')
# # #         except Exception as e:
# # #             node.get_logger().error(f'Service call failed: {e}')

# # #     future.add_done_callback(response_received_callback)

# # # def main(args=None):
# # #     rclpy.init(args=args)
# # #     node = rclpy.create_node('node_b')
    
# # #     # Create the Server: Listen on '/ping_worker'
# # #     server = node.create_service(Trigger, 'ping_worker', worker_service_callback)
    
# # #     # Create the Client: Targets the '/ping_coordinator' service hosted by Node A
# # #     client = node.create_client(Trigger, 'ping_coordinator')
    
# # #     node.get_logger().info('Node B (Worker Service Node) has started!')
    
# # #     # Trigger a timer to call Node A's service 5 seconds after starting
# # #     node.create_timer(5.0, lambda: call_coordinator_service(node, client))
    
# # #     try:
# # #         rclpy.spin(node)
# # #     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# # #         pass
# # #     finally:
# # #         node.destroy_node()
# # #         rclpy.shutdown()

# # # if __name__ == '__main__':
# # #     main()





# # import rclpy
# # from example_interfaces.srv import Trigger


# # def main(args = None):
# #     rclpy.init(args=args)
# #     node = rclpy.create_node('minimal_client')

# #     client  = node.create_client(Trigger, 'ping_service')

# #     while not client.wait_for_service(timeout_sec=0.1):
# #         node.get_logger().info('Wait for teh server to come live .....')

# #     def response_callback(future):
# #         result = future.result()
# #         node.get_logger().info(f'Server Answered: "{result.message}"')
# #         rclpy.shutdown()

# #     req = Trigger.Request() # Generating a blank request
# #     node.get_logger().info('Sending Request .....')

# #     Future = client.call_async(req)
# #     Future.add_done_callback(lambda fut:response_callback(fut))

# #     # rclpy.spin_until_future_complete(node, Future)
# #     # result = Future.result()
# #     # node.get_logger().info(f'Server Answered:"{result.message}"')
# #     # rclpy.shutdown()

# #     try:
# #         rclpy.spin(node)
# #     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
# #         pass

# # if __name__ == '__main__':
# #     main()


# import rclpy
# from rclpy.action import ActionClient
# from action_tutorials_interfaces.action import Fibonacci

# # --- 1. THE FEEDBACK CALLBACK ---
# def feedback_callback(feedback_msg, node):
#     # This runs every 1 second when the server sends an update
#     current_count = feedback_msg.feedback.sequence[-1]
#     node.get_logger().info(f'[FEEDBACK] Received live count: {current_count}')

# # --- 2. THE FINAL RESULT CALLBACK ---
# def get_result_callback(future, node):
#     result = future.result().result
#     node.get_logger().info(f'[RESULT] Server finished! Final sequence length: {len(result.sequence)}')
#     rclpy.shutdown()

# # --- 3. THE GOAL RESPONSE CALLBACK ---
# def goal_response_callback(future, node):
#     goal_handle = future.result()
#     if not goal_handle.accepted:
#         node.get_logger().info('Goal was rejected by the server.')
#         return

#     node.get_logger().info('Goal accepted! Waiting for the final result...')
    
#     # Ask the server to send the final result once it finishes counting
#     res_future = goal_handle.get_result_async()
#     res_future.add_done_callback(lambda fut: get_result_callback(fut, node))

# def main(args=None):
#     rclpy.init(args=args)
#     node = rclpy.create_node('minimal_action_client')

#     # Create the Action Client
#     client = ActionClient(node, Fibonacci, 'count_to_500')

#     node.get_logger().info('Waiting for Action Server...')
#     client.wait_for_server()

#     # Set the goal (Let's set it to 10 for testing so it doesn't take 500 full seconds!)
#     goal_msg = Fibonacci.Goal()
#     goal_msg.order = 10 

#     node.get_logger().info('Sending goal to count up to 10...')
    
#     # Send the goal asynchronously, linking our feedback callback
#     send_goal_future = client.send_goal_async(
#         goal_msg, 
#         feedback_callback=lambda fb: feedback_callback(fb, node)
#     )
    
#     # Listen for whether the server accepted or rejected the goal
#     send_goal_future.add_done_callback(lambda fut: goal_response_callback(fut, node))

#     try:
#         rclpy.spin(node)
#     except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
#         pass

# if __name__ == '__main__':
#     main()





import rclpy
from my_robot_interfaces.srv import SetLedColor

def response_callback(future, node):
    try:
        result = future.result()
        if result.success:
            node.get_logger().info(f'Client Success!!!!!!!!!!!  {result.message}')
        else:
            node.get_logger().error(f'Clinet Failed !!!!!!! {result.message}')

    except Exception as e:
        node.get_logger().error(f'Service call failed completely: {e}')

    rclpy.shutdown()


def main(args = None):
    rclpy.init()
    node = rclpy.create_node('led_service_client_node')
    client = node.create_client(SetLedColor, 'set_led_color')

    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info(f'Waiting for teh LED service to come ON')

    req = SetLedColor.Request()
    req.color = 'green'

    node.get_logger().info(f'Sending request to {req.color}')

    future = client.call_async(req)

    future.add_done_callback(lambda fut: response_callback(fut, node))

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass

if __name__ == "__main__":
    main()