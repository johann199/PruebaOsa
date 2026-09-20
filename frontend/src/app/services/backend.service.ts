import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Usuario } from './session.service';

export interface EstadoFactura {
  numero_factura: string;
  fecha_vencimiento: string;
  dias_mora: number;
  valor: number;
  estado: string;
}

export interface EstadoCuentaResult {
  cliente: string;
  nit: string;
  total_pendiente: number;
  facturas: EstadoFactura[];
}

export interface ClientePrioritario {
  cliente: string;
  factura: string;
  dias_mora: number;
  promedio_historico: number;
  valor: number;
  score_prioridad: number;
}

export interface Resumen {
  clientes_prioritarios: ClientePrioritario[];
  proyeccion_recaudo: Record<string, number>;
  total_cartera: number;
  cantidad_facturas: number;
}

@Injectable({ providedIn: 'root' })
export class BackendService {
  private readonly api = `${environment.backendUrl}/api`;

  constructor(private readonly http: HttpClient) {}

  login(correo: string, password: string): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.api}/usuario/login`, { correo, password });
  }

  resumenDashboard(): Observable<Resumen> {
    return this.http.get<Resumen>(`${this.api}/dashboard/resumen`);
  }

  estadoCuenta(token: string, nit: string): Observable<EstadoCuentaResult> {
    return this.http.post<EstadoCuentaResult>(`${this.api}/portal-cliente/estado-cuenta/${token}`, { nit });
  }
}