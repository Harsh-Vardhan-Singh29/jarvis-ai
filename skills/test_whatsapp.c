// # import sys
// # import os

// # # add project root to PYTHONPATH
// # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

// # from skills.whatsapp import open_whatsapp, search_contact, send_message

// # print(open_whatsapp())
// # print(search_contact("umang"))
// # print(send_message("Hello from Jarvis 🤖"))
// # if (send_message("Hello from Jarvis 🤖")):
// #     print("Message sent successfully!")


// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>

// unsigned long long hash(const char *str) {
//     unsigned long long hash = 5381;
//     int c;

//     while ((c = *str++))
//         hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

//     return hash;
// }

// int main(){
//     char input[100];
//     printf("Enter a string to hash: ");
//     fgets(input, sizeof(input), stdin);
//     input[strcspn(input, "\n")] = 0; // Remove newline character
//     printf("Hash value: %llu\n", hash(input));
// }



