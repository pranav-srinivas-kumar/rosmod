#include <iostream>
#include <fstream>
#include <string>
#include "KRPC.pb.h"

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <google/protobuf/io/zero_copy_stream.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/io/coded_stream.h>
using namespace google::protobuf::io;

#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <ifaddrs.h>

#include <cstring>      // std::memcpy
#include <algorithm>    // std::swap
#include <memory>

using namespace std;

const int maxBufferSize = 65535;

// This function fills in a Argument message based on user input.
void PromptForArgument(krpc::Argument* argument) {
  unsigned int position;
  cout << "Input position for argument: ";
  cin >> position;
  argument->set_position(position);
  cin.ignore(256, '\n');
  
  cout << "Input value for the argument (as a string): ";
  string value;
  getline(cin, value);
  argument->set_value(value);
}

// Main function:  Reads the entire address book from a file,
//   adds one argument based on user input, then writes it back out to the same
//   file.
int main(int argc, char* argv[]) {
  // Verify that the version of the library that we linked against is
  // compatible with the version of the headers we compiled against.
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  krpc::Request request;
  string fileName;
  if (argc == 2)
  {
    fileName = argv[1];
    // Read the existing address book.
    fstream input(fileName.c_str(), ios::in | ios::binary);
    if (!input) {
      cout << fileName << ": File not found.  Creating a new file." << endl;
      cout << "Enter service name: ";
      string service;
      getline(cin, service);
      request.set_service(service);

      cout << "Enter procedure name: ";
      string procedure;
      getline(cin, procedure);
      request.set_procedure(procedure);
    } else if (!request.ParseFromIstream(&input)) {
      cerr << "Failed to parse request." << endl;
      return -1;
    } else {
      cout << "Service name: " << request.service() << endl;
      cout << "Service procedure name: " << request.procedure() << endl;
      for (int i=0; i < request.arguments_size(); i++)
	{
	  const krpc::Argument& argument = request.arguments(i);
	  cout << "Argument position: " << argument.position() << endl;
	  cout << "Argument value: " << argument.value() << endl;
	}
    }
  } 
  else
    {
      cout << "Enter service name: ";
      string service;
      getline(cin, service);
      request.set_service(service);

      cout << "Enter procedure name: ";
      string procedure;
      getline(cin, procedure);
      request.set_procedure(procedure);
      fileName = service + "." + procedure;
    }

  // Add an service.

  while (true)
    {
      cout << "Add argument (Y/N)? ";
      char result;
      cin >> result;
      if (result == 'Y')
	{
	  cin.ignore(256, '\n');
	  PromptForArgument(request.add_arguments());
	}
      else
	break;
    }

  /* SEND DATA TO KRPC SERVER */
  {
    int sockfd;
    u_short server_portno = 50000;
    char server_ip_str[] = "127.0.0.1";
  
    /* socket: create the socket */
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) <0) {
      perror("ERROR opening socket");
    }
    /* build the server's Internet address */
    struct sockaddr_in server_addr;    
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_portno);
    if (inet_pton(AF_INET, server_ip_str, &(server_addr.sin_addr)) !=1) {
      perror("inet_pton");
    }
    /* set the address to zero */
    memset(server_addr.sin_zero, 0, sizeof server_addr.sin_zero);
    /* connect: create a connection with the server */
    if (connect(sockfd, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0) {
      perror("ERROR connecting");
    }
    /* set the timeout on the socket receive */
    struct timeval tv;
    tv.tv_sec = 10;
    tv.tv_usec = 0;
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO,&tv,sizeof(tv)) < 0) {
      perror("Couldn't set sockopts!");
      close(sockfd);
    }
    /* send the message line to the server */
    int sentbytes=0,numbytes=0;
    char hellobuf[] = {
      0x48, 0x45, 0x4C, 0x4C, 0x4F, 0x2D, 0x52, 0x50, 0x43, 0x00, 0x00, 0x00
    };
    if ( numbytes = send(sockfd, hellobuf, 12,0) == -1) {
      perror("send");
    }
    char connID[32] = "testKRPC_program";
    if ( numbytes = send(sockfd, connID, 32,0) == -1) {
      perror("send");
    }
    bool haveReceivedID = false;
    char clientID[16];
    while (!haveReceivedID)
      {
	memset(clientID,0,16);
	int bytesreceived =0;
	if ( (bytesreceived=recv(sockfd,clientID,16,0)) <= 0) {
	  perror("recv");
	}
	else {
	  std::cout << "RECEIVED UNIQUE CLIENT ID: " << clientID << endl;
	  haveReceivedID = true;
	}
      }
    string message;
    message.reserve(maxBufferSize);
    uint64_t size;
    if (request.SerializeToString(&message))
      {
	/* write the length of the serialized message */
	std::cout << "Converting message length " << message.length() << " to Varint64" << endl;
	unsigned char messageLen[10];
	CodedOutputStream::WriteVarint64ToArray(message.length(), messageLen);
	/* create the full data packet and send it */
	string msg = string((const char *)messageLen) + message;
	if ( numbytes = send(sockfd, msg.data(), msg.length(), 0) == -1) {
	  perror("send");
	}
	std::cout << "Sent message of length: " << msg.length() << endl;	
	/* receive the response from the server */
	char buf[maxBufferSize];
	memset(buf,0,maxBufferSize);
	int bytesreceived =0;
	if ( (bytesreceived=recv(sockfd,buf,maxBufferSize-1,0)) <= 0) {
	  perror("recv");
	}
	std::cout << "Received " << bytesreceived << " bytes" << endl;
	ZeroCopyInputStream* raw_input = new ArrayInputStream(buf,maxBufferSize);
	CodedInputStream* coded_input = new CodedInputStream(raw_input);
	coded_input->ReadVarint64(&size);
	std::cout << "Received a return message of length: " << size << std::endl;
	krpc::Response response;
	if (response.ParseFromCodedStream(coded_input))
	  {
	    std::cout << "Got Response message" << endl;
	    std::cout << "Response time: " << response.time() << endl;
	    if ( response.has_error() )
	      std::cout << "Response error: " << response.error() << endl;
	    std::cout << "Response return_value length: " << response.return_value().length() << endl;
	    ZeroCopyInputStream* byte_input = new ArrayInputStream(response.return_value().data(), response.return_value().length());
	    CodedInputStream* coded_services = new CodedInputStream(byte_input);
	    krpc::Services services;
	    if (services.ParseFromCodedStream(coded_services))
	      {
		std::cout << "Got Services message" << endl;
		std::cout << "Got " << services.services_size() << " services" << endl;
		for (int i=0;i<services.services_size();i++)
		  {
		    const krpc::Service& service = services.services(i);
		    std::cout << "Service " << i << ":" << endl;
		    std::cout << "\tName: " << service.name() << endl;
		    std::cout << "\tProcedures Count: " << service.procedures_size() << endl;
		    for (int j=0;j<service.procedures_size();j++)
		      {
			const krpc::Procedure& procedure = service.procedures(j);
			std::cout << "\tProcedure " << j << ":" << endl;
			std::cout << "\t\tName: " << procedure.name() << endl;
			std::cout << "\t\tParameters Count: " << procedure.parameters_size() << endl;
			for (int k=0;k<procedure.parameters_size();k++)
			  {
			    const krpc::Parameter& parameter = procedure.parameters(k);
			    std::cout << "\t\tParameter " << k << ":" << endl;
			    std::cout << "\t\t\tName: " << parameter.name() << endl;
			    std::cout << "\t\t\tType: " << parameter.type() << endl;
			    if (parameter.has_default_argument())
			      std::cout << "\t\t\tDefault Argument: " << parameter.default_argument() << endl;
			  }
			if (procedure.has_return_type())
			  std::cout << "\t\tReturn Type: " << procedure.return_type() << endl;
		      }
		    std::cout << "\tClasses Count: " << service.classes_size() << endl;
		    std::cout << "\tEnumerations Count: " << service.enumerations_size() << endl;
		  }
	      } else
	      {
		std::cout << "Response return_value: " << response.return_value() << endl;
	      }
	    delete coded_services;
	    delete byte_input;
	  }

	delete coded_input;
	delete raw_input;
      } else
      {
	std::cerr << "Couldn't serialize message!" << endl;
      }

    close(sockfd);
  }
  
  {
    // Write the new request back to disk.
    fstream output(fileName.c_str(), ios::out | ios::trunc | ios::binary);
    if (!request.SerializeToOstream(&output)) {
      cerr << "Failed to write request." << endl;
      return -1;
    }
  }

  // Optional:  Delete all global objects allocated by libprotobuf.
  google::protobuf::ShutdownProtobufLibrary();

  return 0;
}
