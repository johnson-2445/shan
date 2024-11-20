#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>

#define MAX_PACKET_SIZE 1024

typedef struct {
    char *ip_address;
    int port;
    int interval_ms;
    int num_packets;
    int thread_id;
} thread_params;

void *send_packet(void *params) {
    thread_params *thread_data = (thread_params *)params;
    int sock;
    struct sockaddr_in server_addr;
    const char *packet_data = "@MoinOwner";  
    int packet_size = strlen(packet_data);     

    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        fprintf(stderr, "Socket creation failed\n");
        return NULL;
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(thread_data->port);

    if (inet_pton(AF_INET, thread_data->ip_address, &server_addr.sin_addr) <= 0) {
        fprintf(stderr, "Invalid IP address: %s\n", thread_data->ip_address);
        close(sock);
        return NULL;
    }

    for (int i = 0; i < thread_data->num_packets; i++) {
        ssize_t sent = sendto(sock, packet_data, packet_size, 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
        if (sent == -1) {
            fprintf(stderr, "Packet send failed in thread %d\n", thread_data->thread_id);
            close(sock);
            return NULL;
        }
        printf("Thread %d: Packet sent to %s:%d\n", thread_data->thread_id, thread_data->ip_address, thread_data->port);
        usleep(thread_data->interval_ms * 1000);  
    }

    close(sock);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s [IP] [PORT] [TIME] [PACKET_RATE]\n", argv[0]);
        return 1;
    }

    char *ip_address = argv[1];
    int port = atoi(argv[2]);
    int duration = atoi(argv[3]);
    int packet_rate = atoi(argv[4]); 

    int num_threads = 5;  
    int packets_per_thread = packet_rate * duration / num_threads;
    int interval_ms = 1000 / packet_rate;

    pthread_t threads[num_threads];
    thread_params params[num_threads];

    printf("Starting packet sender with %d threads...\n", num_threads);

    for (int i = 0; i < num_threads; i++) {
        params[i] = (thread_params) { ip_address, port, interval_ms, packets_per_thread, i + 1 };
        if (pthread_create(&threads[i], NULL, send_packet, &params[i]) != 0) {
            fprintf(stderr, "Thread creation failed for thread %d\n", i + 1);
            return 1;
        }
        printf("Thread %d started\n", i + 1);
    }

    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("All threads completed. Packets sent at a rate of %d packets/second.\n", packet_rate);
    return 0;
}
