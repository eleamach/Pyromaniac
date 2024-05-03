// Date: 19/12/2023
// Version: 1.0
// Author: Eléa Machillot



// Includes
#include "MicroBit.h"
#include <aes.hpp>
#include <string>
#include <vector>




// Global variables
MicroBit uBit;
const uint8_t my_AES_key[16] = "dnwatriom";



// Function to convert a character array to a uint8_t array
void convertion_en_uint(char* in, int size, uint8_t* out) 
{
    for (int i = 0; i < size; i++) 
    {
        out[i] = (uint8_t)in[i];
    }
}



// Function to convert a uint8_t array to a character array
void convertion_en_char(uint8_t* in, int size, char* out) 
{
    for (int i = 0; i < size; i++) 
    {
        out[i] = (char)in[i];
    }
    out[size] = '\0';  // Ensure null termination
}




// Function for encryption using AES
char* encryption(ManagedString src)
{
    uint8_t data[16];
    char* received = (char*)malloc(17*sizeof(char)); //Allocating memory for a character array of 17
    for(int i=0; i<16; i++)
    {
        received[i] = src.charAt(i); //Received contains the first 16 characters of the string
    }
    convertion_en_uint (received,16,data); // Convert characters to uint8_t array,
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, my_AES_key);
    AES_ECB_encrypt(&ctx, data); // Then encrypt the data using AES in ECB mode back to characters
    convertion_en_char(data,16, received);
    return received;
}


// Function to split a ManagedString into a vector of std::string using a delimiter
char** splitManagedString(char* input, int size, const std::string& delimiter) 
{
    char** result = (char**)malloc(16 * sizeof(char*)); // 16 is the maximum number of part of a message that can be sent
    memset(result, 0, 16 * sizeof(char*));
    char* start = input; // Start of the message
    int idx = 0; // Index of the current part of the message
    for(int i = 0; i < size; i++)  // Loop through the message
    {
        if(strncmp(input + i, delimiter.c_str(), delimiter.length()) == 0)  // If the delimiter is found
        {
            result[idx++] = start; // Add the part of the message to the vector
            start = input + i + delimiter.length(); // Update the start of the message to after the delimiter
        }
    }
    result[idx++] = start; // Add the last part of the message to the vector
    return result;
}
// Function to receive a message when a radio event is detected
void onData(MicroBitEvent) 
{
    const std::string separator = ":";
    PacketBuffer data_read_radio = uBit.radio.datagram.recv(); // Read the message
    char* data_encrypted = (char*)data_read_radio.getBytes(); // Convert the ManagedString to a character array

    char** test = splitManagedString(data_encrypted,data_read_radio.length() , separator); // Split the message into parts
    if ( (strncmp(data_encrypted,"1857",4) == 0) && (*test[1] == 'S') && (*test[3] == 'r')){


        uBit.serial.send('s');
    }
    
    free(test);
    

}

// Main
int main()
{
    // Initialisation
    uBit.init();
    uBit.radio.enable();
    uBit.serial.baud(115200);
    uBit.messageBus.listen(MICROBIT_ID_RADIO, MICROBIT_RADIO_EVT_DATAGRAM, onData);
    uBit.serial.setRxBufferSize(60); 
    PacketBuffer packet(248);
    ManagedString data;
    
    int N = 11;
    int idProtocole = 1857;
    int idPasserel = 1;
    char type = 'G';
    char startData[N+1]; 

    std::sprintf(startData, "%d:%c:%d::", idProtocole, type, idPasserel);
    

    
    while (1) {
        char receivedChar;
        char* data_encode = NULL;
        size_t len = 5;
        while ((receivedChar = uBit.serial.read()) != -1) // While there is data to read
        {
            data = data + receivedChar; // Add the character to the string
            uBit.serial.send(receivedChar);
            if (data.length()==14) // If the string is 14 characters long
            {
                len += 16;
                data_encode = (char*)realloc(data_encode, len+5+1); // Allocate memory for the string
                char * encrypted_data = encryption(data); 
                memcpy(data_encode + len - 16 , encrypted_data, 16); // Copy the encrypted string to the data_encode string
                free(encrypted_data); 
                memcpy(data_encode + len, "+*_*+", 5); // Add the separator
                len += 5; // Add the length of the separator to the length of the string
                data = "";
            }
            if (receivedChar == '}') // If the character is '}', wich mean the end of the json
            {
                len += 16;
                data_encode = (char*)realloc(data_encode, len+1+N); // Allocate memory for the string
                char * encrypted_data = encryption(data); 
                memcpy(data_encode + len - 16 , encrypted_data, 16); // Copy the encrypted string to the data_encode string
                free(encrypted_data);
                memcpy(packet.getBytes(), data_encode, len); // Copy the string to the packet
                uBit.radio.datagram.send(packet); // Send the packet
                //uBit.serial.send("s"); // Send a character to the microbit_pass to tell him that the message has been sent
                data = "";
                free(data_encode);
                len = N; 
                data_encode = (char*)malloc(len+1); // Allocate memory for the string
                memcpy(data_encode, startData, N); // Add the header

 
            }
        }
    }
}