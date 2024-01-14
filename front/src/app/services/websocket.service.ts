import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  private socket$: WebSocket;
  private readonly url = 'ws://0.0.0.0:8000/ws';

  constructor() {
      this.socket$ = new WebSocket(this.url);
  }

  connect(): Subject<MessageEvent> {
    const observable = new Observable(observer => {
      this.socket$.addEventListener('message', event => observer.next(event));
      this.socket$.addEventListener('error', error => observer.error(error));
      this.socket$.addEventListener('close', () => observer.complete());
      return () => this.socket$.close();
    });

    const observer = {
      next: (data: any) => {
        if (this.socket$.readyState === WebSocket.OPEN) {
          this.socket$.send(JSON.stringify(data));
        }
      }
    };

    return Subject.create(observer, observable);
  }

  closeConnection() {
    this.socket$.close();
  }

}
