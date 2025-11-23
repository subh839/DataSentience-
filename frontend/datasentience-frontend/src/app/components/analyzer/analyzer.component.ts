import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';

import { DatasentienceService, AnalysisResponse } from '../../services/datasentience.service';

@Component({
  selector: 'app-analyzer',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatButtonModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatListModule,
    MatIconModule
  ],
  templateUrl: './analyzer.component.html',
  styleUrl: './analyzer.component.scss'
})
export class AnalyzerComponent {
  private datasentienceService = inject(DatasentienceService);
  
  query = '';
  isLoading = signal(false);
  result = signal<AnalysisResponse | null>(null);
  error = signal('');

  async analyze() {
    if (!this.query.trim()) return;

    this.isLoading.set(true);
    this.error.set('');
    this.result.set(null);

    try {
      const response = await this.datasentienceService.analyzeQuery(this.query).toPromise();
      this.result.set(response!);
    } catch (err) {
      this.error.set('Analysis failed. Please check if the backend server is running.');
      console.error('Analysis error:', err);
    } finally {
      this.isLoading.set(false);
    }
  }

  getSeverityColor(severity: string): string {
    const colors: { [key: string]: string } = {
      'Low': 'text-green-600',
      'Medium': 'text-yellow-600',
      'High': 'text-orange-600',
      'Critical': 'text-red-600'
    };
    return colors[severity] || 'text-gray-600';
  }

  getSeverityBadgeColor(severity: string): string {
    const colors: { [key: string]: string } = {
      'Low': 'bg-green-100 text-green-800',
      'Medium': 'bg-yellow-100 text-yellow-800',
      'High': 'bg-orange-100 text-orange-800',
      'Critical': 'bg-red-100 text-red-800'
    };
    return colors[severity] || 'bg-gray-100 text-gray-800';
  }
}