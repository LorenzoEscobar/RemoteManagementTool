# RemoteManagementTool

A remote management tool that allows terminal access to multiple clients at a given time. Using Python sockets, a connection is established between the server and client. The server can list clients connected, select a client, and send commands in their terminal and recieve any output. The server can also disconnect from the client and connect to another client easily without destroying any connections.

### Instructions
- For now, Python3 must be installed on both the server and client computers. (I will later make these executables so this will not be an issue in the future)
- The Server file goes on the computer you would like to manage connections from, make sure the necessary ports are open on this computer.
- The Server file must be kept open in order for connections to be established. If closed, you will lose your connections and the clients must be relaunched.
- The Client file goes on client computers you would like to manage, make you change your `host` string to the ip of your Server computer.
- To disconnect from the client you must use #quit
### Commands on the server can be seen with 'help' and on the client can be seen with #help
