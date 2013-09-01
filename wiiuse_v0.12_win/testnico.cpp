#include <stdio.h>
#include <stdlib.h>
#include "wiiuse.h"

#define NUMBER_OF_REMOTES 1
void handle_event(struct wiimote_t* rm){

    if(IS_PRESSED(rm, WIIMOTE_BUTTON_UP)){
        printf("\n - IR Activated - \n");
        wiiuse_set_ir(rm,1);
    }
    else if(IS_PRESSED(rm, WIIMOTE_BUTTON_DOWN)){
        printf("\n - IR Dectivated - \n");
        wiiuse_set_ir(rm,0);
    }

    if(WIIUSE_USING_IR(rm)){

        for(int i=0; i<4; i++){
            if(rm->ir.dot[i].visible){
                printf("IR source %i: (%u, %u)\n", i, rm->ir.dot[i].x, rm->ir.dot[i].y);
            }
            printf("IR cursor: (%u, %u)\n", rm->ir.x, rm->ir.y);
            printf("IR z distance: %f\n", rm->ir.z);

        }
    }
}

void handle_disconnect(struct wiimote_t* rm){
    printf("\n - DISCONNECTED - ID: %i\n\n", rm->unid);
}

int main()
{
    wiimote**  remote = wiiuse_init(NUMBER_OF_REMOTES);
    printf("Searching...");
    int found = wiiuse_find(remote, NUMBER_OF_REMOTES, 5000);
    printf("Found %d devices\n", found);
    int connected = wiiuse_connect(remote, found);

    if(!connected){
        printf("Failed to connect\n");
        return 0;
    }
    else{

        printf("Connected\n");
        wiiuse_rumble(remote[0],1);
        Sleep(250);
        wiiuse_rumble(remote[0],0);

        while(1){
            if (wiiuse_poll(remote, NUMBER_OF_REMOTES)) {
                for(int i=0;i<NUMBER_OF_REMOTES; i++){
                    switch(remote[i]->event){
                        case WIIUSE_EVENT:
                                   handle_event(remote[i]); break;

                        case WIIUSE_DISCONNECT:
                        case WIIUSE_UNEXPECTED_DISCONNECT:
                                   handle_disconnect(remote[i]); break;
                        default: break;
                    }
                }
            }
        }
        wiiuse_cleanup(remote,NUMBER_OF_REMOTES);
    }
}