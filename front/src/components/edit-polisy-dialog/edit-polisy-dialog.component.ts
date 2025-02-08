import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-edit-polisy-dialog',
  templateUrl: './edit-polisy-dialog.component.html',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
  styleUrls: ['./edit-polisy-dialog.component.scss'],
})
export class EditPolisyDialogComponent implements OnInit {
  editForm!: FormGroup;

  constructor(
    private fb: FormBuilder,  
    public dialogRef: MatDialogRef<EditPolisyDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any // Data passed from the parent component
  ) {}

  ngOnInit(): void {
    // Initialize the form with the data passed to the dialog
    this.editForm = this.fb.group({
      pesel: [this.data?.element?.pesel || '', [Validators.required]],
      firstName: [this.data?.element?.firstName || '', [Validators.required]],
      lastName: [this.data?.element?.lastName || '', [Validators.required]],
      policyValue: [this.data?.element?.policyValue || '', [Validators.required, Validators.min(1)]],
      startDate: [this.data?.element?.startDate || '', [Validators.required]],
      endDate: [this.data?.element?.endDate || '', [Validators.required]],
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
