import { Component,  OnInit } from '@angular/core';
import { WebsocketService } from '../../services/websocket.service';
import { NgxChartsModule } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NgxChartsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {

  messages: any[] = [];
  messageToSend: string = "";

  xAxisLabel: string = '';
  yAxisLabel: string = '';
  view: [number,number] = [1000,800];
  data: any[] = [];

  legend: boolean = true;
  legendTitle: string = "";
  animations: boolean = true;
  xAxis: boolean = true;
  yAxis: boolean = true;
  showYAxisLabel: boolean = true;
  showXAxisLabel: boolean = true;
  timeline: boolean = true;

  allDataPoints: any[] = [];

  constructor(private websocketService: WebsocketService) {
    
    this.data = [
      {
        name: 'Model',
        showYAxisLabel: this.showYAxisLabel,
        xAxisLabel: 'seconds',
        yAxisLabel: 'loss',
        legendTitle: "Modelo",
        series: [
          {
            "name": 0,  // x
            "value": 0.0  // y
          },
        ] // Initialize series as an empty array
      }
    ];

   }

  ngOnInit(): void {
    const socket = this.websocketService.connect();

    socket.subscribe({
      next: (message: any) => {
        console.log(message.data)

        const dataType = typeof message.data;
        console.log('Data type:', dataType);

        const dataObject = JSON.parse(message.data);
        console.log('Received data as object 1 item with 5 elements:', dataObject);

        const seconds = parseFloat(dataObject.data[1]); // Accessing value at index 1
        console.log(seconds);

        const loss = parseFloat(dataObject.data[2]);
        console.log(loss)

        if (!isNaN(seconds) && !isNaN(loss)) {
          // Update this.messages
          this.messages.push([seconds, loss]);  
          this.allDataPoints.push({ name: seconds, value: loss });
          this.data = [
            {
              series: this.allDataPoints,
              name: 'Model',
            }
          ];  

          console.log(this.data);
        } else {
          console.error('Invalid data received from websocket');
        }
      
      },
      error: (error: any) => {
        console.error('Error:', error);
      }
    });
  }

  ngOnDestroy() {
    this.websocketService.closeConnection();
  }

}
