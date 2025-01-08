### INTRODUCTION ###

The python example should give you a quick intro at how to use the given network protocol based on the grpc framework.
However, we, the teaching staff, don't give any support regarding the use and setup of this example.
Any questions regarding "it does not run", "what does this code do" or such will not be answered.
Reporting of errors and mistakes is always welcome.
Note, that you have to edit the examples first (in code), before you can properly use them.

The network protocol is defined in the '.proto' files.
The main file is the 'netcode.proto', which contains all available remote procedure calls.
The other files are game-specific implementations, which are used inside the 'netcode.proto'.

- Use the 'gen-python-netcode.sh' script to generate the python netcode.
- To use the script some setup is required, please refer to https://grpc.io/docs/languages/python/quickstart/ (gRPC, gRPC tools)

Note, that you don't have to use this example or python for the practical, it exists to give you an introduction of a client structure.
Keep in mind, having a beautiful and well-structured client/agent won't give you extra points, but it will be easier to explain the code to tutors.


### PYTHON, HOW TO RUN ###

1. './gen-python-netcode ./protobuf ./netcode'
2. 'python main.py'
3. Cry, it will not work, because the UserToken is not configured. However, I am sure you will be able to fix that ;)
