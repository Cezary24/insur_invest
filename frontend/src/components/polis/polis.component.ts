import { ChangeDetectorRef, Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import {  MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { EditPolisyDialogComponent } from '../edit-polisy-dialog/edit-polisy-dialog.component';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { PolisResponse } from '../../models/polis_response';
import { SpinnerComponent } from '../spinner/spinner.component';

@Component({
  selector: 'app-polis',
  imports: [ MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    ReactiveFormsModule, 
    HttpClientModule  ,
    MatCardModule,MatTableModule,
    EditPolisyDialogComponent,
    MatDialogModule],
  templateUrl: './polis.component.html',
  styleUrls: ['./polis.component.scss']
})
export class PolisComponent {
  polisForm: FormGroup;
  selectedFiles: File[] = [];
  policiesData: PolisResponse[] = [];
  displayedColumns: string[] = [
    'pesel', 
    'insuredFirstName', 
    'insuredLastName', 
    'amount', 
    'insuranceCompany', 
    'policyCategory', 
    'actions'
  ];
  dataSource = new MatTableDataSource<PolisResponse>([]);

  constructor(private fb: FormBuilder, 
    private http: HttpClient, 
    private dialog: MatDialog, 
    private cdref:ChangeDetectorRef) {
    this.polisForm = this.fb.group({});
  }

  onFilesSelected(event: any): void {
    this.selectedFiles = Array.from(event.target.files);
  }

  async onSubmit(): Promise<void> {
    if (this.selectedFiles.length === 0) {
      return;
    }

    const dialogRef = this.dialog.open(SpinnerComponent, {
      disableClose: true, 
      panelClass: 'spinner-dialog'
    });

    for (const file of this.selectedFiles) {
      try {
        const policyData = await this.processFile(file);
        const processedJson = policyData.processed_json;
        const response: PolisResponse = {
          insuredFirstName: processedJson["dane ubezpieczonego"].imie,
          insuredLastName: processedJson["dane ubezpieczonego"].nazwisko,
          pesel: processedJson["dane ubezpieczonego"]["PESEL/REGON"],
          amount: processedJson["wysokosc skladki"],
          insuranceCompany: processedJson["marka towarzystwa ubezpieczeniowego"],
          policyCategory: processedJson["kategoria polisy"]
        };
        
        this.dataSource.data = [...this.dataSource.data, response];
        console.log(this.dataSource.data);
      } catch (error) {
        console.error(`Error processing file ${file.name}:`, error);
      }
    }
    dialogRef.close(); 
  }

  private async processFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('name', "nazwa");
    formData.append('file', file);
    const url = 'http://127.0.0.1:8000/polis/';
    return this.http.post<any>(url, formData).toPromise();
  }


  onEdit(element: PolisResponse): void {
    const dialogRef = this.dialog.open(EditPolisyDialogComponent, {
      width: '400px',
      data: { element: element }, 
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result) {
        const index = this.dataSource.data.findIndex(polis => polis.pesel === element.pesel);
        if (index !== -1) {
          this.dataSource.data[index] = { ...this.dataSource.data[index], ...result };
          this.dataSource.data = [...this.dataSource.data];
        }
      }
    });
  }
}
