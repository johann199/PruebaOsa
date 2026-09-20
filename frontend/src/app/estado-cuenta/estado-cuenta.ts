import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { BackendService, EstadoCuentaResult } from '../services/backend.service';

@Component({
  imports: [FormsModule, DatePipe],
  selector: 'app-estado-cuenta',
  styleUrl: './estado-cuenta.scss',
  templateUrl: './estado-cuenta.html',
})
export class EstadoCuenta {
  readonly nit = signal('');
  readonly estadoCuenta = signal<EstadoCuentaResult | null>(null);
  readonly cargando = signal(false);
  readonly error = signal('');

  private readonly token: string;

  constructor(
    private readonly backend: BackendService,
    private readonly route: ActivatedRoute,
  ) {
    this.token = this.route.snapshot.paramMap.get('token') ?? '';
  }

  consultar() {
    this.error.set('');
    this.cargando.set(true);
    this.backend.estadoCuenta(this.token, this.nit()).subscribe({
      next: (datos) => {
        this.estadoCuenta.set(datos);
        this.cargando.set(false);
      },
      error: (e) => {
        this.cargando.set(false);
        this.estadoCuenta.set(null);
        if (e.status === 403) {
          this.error.set('El NIT no corresponde a este enlace. Verifícalo e inténtalo de nuevo.');
        } else if (e.status === 404) {
          this.error.set('El enlace de estado de cuenta no es válido.');
        } else {
          this.error.set('No se pudo consultar el estado de cuenta. Inténtalo más tarde.');
        }
      },
    });
  }

  volver() {
    this.estadoCuenta.set(null);
    this.error.set('');
  }

  formatoCOP(valor: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      maximumFractionDigits: 0,
    }).format(valor ?? 0);
  }
}