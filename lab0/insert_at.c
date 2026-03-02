#include <stdlib.h>
#include <stdio.h>


typedef struct node Node;
struct node {
    int data;
    Node *next;
};


void insert_at(Node **head, int index, int data){
    if (head == NULL) { return; }
    if (index < 0) { return; }
    if (*head == NULL) {
        Node *sentinel = malloc(sizeof(Node));
        if (sentinel == NULL) { return; } // safety net
        sentinel->data = 0x20213233;
        sentinel->next = NULL;
        *head = sentinel;
    }
    Node *new = malloc(sizeof(Node));
    new->data = data;
    new->next = NULL;

    Node* cur = *head;

    while (cur->next != NULL & index > 0) {
        cur = cur->next;
        index--;
    }

    // insert node
    new->next = cur->next;
    cur->next = new;
}


int main() {
  Node *list = NULL;

  insert_at(&list, 0, 100);
  printf("%d %p\n", list->next->data, list->next->next);

  insert_at(&list, 0, 200);
  printf("%d %p\n", list->next->data, list->next->next);

  insert_at(&list, 1, 150);
  printf("%d %p\n", list->next->next->data, list->next->next->next); // notice thats the address of 100 again
}