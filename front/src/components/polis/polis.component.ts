import { ChangeDetectorRef, Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import {  MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { EditPolisyDialogComponent } from '../edit-polisy-dialog/edit-polisy-dialog.component';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

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
  policiesData: any[] = [];
  displayedColumns: string[] = ['pesel', 'firstName', 'lastName', 'policyValue', 'startDate', 'endDate', 'actions'];

  constructor(private fb: FormBuilder, private http: HttpClient, private dialog: MatDialog, private cdref:ChangeDetectorRef) {
    this.polisForm = this.fb.group({});
  }

  onFilesSelected(event: any): void {
    this.selectedFiles = Array.from(event.target.files);
  }

  async onSubmit(): Promise<void> {
    if (this.selectedFiles.length === 0) {
      return;
    }

    for (const file of this.selectedFiles) {
      try {
        const policyData = await this.processFile(file);
        this.policiesData.push(policyData);
      } catch (error) {
        console.error(`Error processing file ${file.name}:`, error);
      }
    }
  }

  private async processFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('name', "nazwa");
    formData.append('file', file);
    const url = 'http://127.0.0.1:8000/polis/';
    //return this.http.post<any>(url, formData).toPromise();

    return {
      name: "nazwa",
      surname: "nazwisko",
      pesel: "12345678901",
      price: "100",
      endDate: "2024-01-01"
    }
  }


  onEdit(element: any): void {
    const dialogRef = this.dialog.open(EditPolisyDialogComponent, {
      width: '400px',
      data: { element: element }, 
    });

    dialogRef.afterClosed().subscribe((result: any) => {

        if (result) {
          const index = this.policiesData.findIndex(polis => polis.pesel === element.pesel);
        if (index !== -1) {
          this.policiesData[index] = { ...this.policiesData[index], ...result };
        }
        this.cdref.detectChanges();
      }
    });
  }
}
