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
    out[size] = '\0'; // Ensure null termination
}



// Function for decryption using AES
ManagedString decryption(char* src)
{
    uint8_t data[16];
    char received[17];
    convertion_en_uint (src,16,data); // Convert characters to uint8_t array,
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, my_AES_key);
    AES_ECB_decrypt(&ctx, data); // Then decrypt the data using AES in ECB mode back to characters
    convertion_en_char(data,16, received);
    return ManagedString(received);
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
    PacketBuffer data_read_radio = uBit.radio.datagram.recv(); // Read the message
    const std::string separator = "+*_*+";
    ManagedString dataEncrypted((const char*)data_read_radio.getBytes(), data_read_radio.length()); // Convert the message to a ManagedString
    char* data_encrypted = (char*)data_read_radio.getBytes(); // Convert the ManagedString to a character array
    char* data_payload = data_encrypted + 11; // Remove the header of the message
    if (strncmp(data_encrypted,"1857:",5) == 0) // If the header is correct
    {
        char** test = splitManagedString(data_payload,data_read_radio.length() -11, separator); // Split the message into parts
        int i = 0;
        while(test[i] != NULL)  // Loop through the parts of the message
        {
            ManagedString data_decrypted = decryption(test[i]); // Decrypt the part of the message
            char data_decrypted_cstr[60];  // Create a character array to store the decrypted part of the message
            strncpy(data_decrypted_cstr, data_decrypted.toCharArray(), sizeof(data_decrypted_cstr)); // Convert the ManagedString to a character array
            data_decrypted_cstr[sizeof(data_decrypted_cstr) - 1] = '\0'; // Ensure null termination
            uBit.serial.send(data_decrypted_cstr); 
            i++; 
        }
        uBit.radio.datagram.send("1857:S:1:r"); // Send an ACK to the sender
        free(test);
        uBit.serial.send("\n\r");
    }
}



// Main
int main() 
{
    // Initialisation
    uBit.init();
    uBit.radio.enable();
    uBit.serial.baud(115200);
    uBit.messageBus.listen(MICROBIT_ID_RADIO, MICROBIT_RADIO_EVT_DATAGRAM, onData);
    while (1) {
        uBit.sleep(1);
    }
    release_fiber(); // Release the fiber to avoid errors
}