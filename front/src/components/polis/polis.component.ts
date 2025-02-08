import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import {  MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-polis',
  imports: [ MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    ReactiveFormsModule,
    HttpClientModule  ,
    MatCardModule,MatTableModule],
  templateUrl: './polis.component.html',
  styleUrls: ['./polis.component.scss']
})
export class PolisComponent {
  polisForm: FormGroup;
  selectedFiles: File[] = [];
  policiesData: any[] = [];
  displayedColumns: string[] = ['pesel', 'firstName', 'lastName', 'policyValue', 'startDate', 'endDate'];

  constructor(private fb: FormBuilder, private http: HttpClient) {
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
    return this.http.post<any>(url, formData).toPromise();
  }
}
