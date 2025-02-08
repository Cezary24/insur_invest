import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';

interface PolicyData {
  pesel: string;
  firstName: string;
  lastName: string;
  policyValue: number;
  startDate: Date;
  endDate: Date;
}

@Component({
  selector: 'app-polis',
  imports: [    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    ReactiveFormsModule,
    MatCardModule],
  templateUrl: './polis.component.html',
  styleUrl: './polis.component.scss'
})
export class PolisComponent {
  polisForm: FormGroup;
  selectedFile: File | null = null;
  selectedFileName: string = '';
  policyData: PolicyData | null = null;

  constructor(private fb: FormBuilder) {
    this.polisForm = this.fb.group({
      name: ['', Validators.required]
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      this.selectedFileName = file.name;
      this.policyData = null; 
    } else {
      this.selectedFile = null;
      this.selectedFileName = '';

    }


  }

  onSubmit(): void {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('name', this.polisForm.get('name')?.value);
      formData.append('file', this.selectedFile);
      


      // Tymczasowe mockowane dane do testów
      this.policyData = {
        pesel: '12345678901',
        firstName: 'Jan',
        lastName: 'Kowalski',
        policyValue: 50000,
        startDate: new Date(),
        endDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1))
      };
    }
  }
}
