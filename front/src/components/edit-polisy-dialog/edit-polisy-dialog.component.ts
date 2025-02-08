import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { PolisResponse } from '../../models/polis_response';
import { MatDialogModule } from '@angular/material/dialog';
import {MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-edit-polisy-dialog',
  templateUrl: './edit-polisy-dialog.component.html',
  imports: [MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    ReactiveFormsModule, 
    MatCardModule,MatTableModule,
    EditPolisyDialogComponent,
    MatDialogModule],
  styleUrls: ['./edit-polisy-dialog.component.scss']
})
export class EditPolisyDialogComponent {
  editForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<EditPolisyDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { element: PolisResponse }
  ) {
    this.editForm = this.fb.group({
      pesel: [this.data.element.pesel, [Validators.required, Validators.pattern(/^\d{11}$/)]],
      insuredFirstName: [this.data.element.insuredFirstName, [Validators.required]],
      insuredLastName: [this.data.element.insuredLastName, [Validators.required]],
      amount: [this.data.element.amount, [Validators.required, Validators.min(0)]],
      insuranceCompany: [this.data.element.insuranceCompany, [Validators.required]],
      policyCategory: [this.data.element.policyCategory, [Validators.required]]
    });
  }

  onSave(): void {
    if (this.editForm.valid) {
      this.dialogRef.close(this.editForm.value);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
