import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface AnalysisResponse {
  query: string;
  context_used: string;
  analysis: {
    root_causes: string[];
    severity: string;
    time_to_failure_hours?: number;
    affected_systems: string[];
    confidence_score: number;
  };
  action_plan: {
    immediate_actions: string[];
    short_term_solutions: string[];
    long_term_recommendations: string[];
    roi_analysis: string;
    timeline: string;
    required_resources: string[];
    estimated_cost_savings: number;
    implementation_costs?: number;
    payback_period_months?: number;
  };
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class DatasentienceService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api';

  analyzeQuery(query: string): Observable<AnalysisResponse> {
    return this.http.post<AnalysisResponse>(`${this.apiUrl}/analyze`, { query });
  }

  healthCheck(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`);
  }
}