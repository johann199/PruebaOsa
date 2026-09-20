import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { BackendService } from '../services/backend.service';
import { SessionService } from '../services/session.service';

@Component({
  imports: [FormsModule],
  selector: 'app-login',
  styleUrl: './login.scss',
  templateUrl: './login.html',
})
export class Login {
  correo = '';
  password = '';
  error = '';
  cargando = false;

  constructor(
    private readonly backend: BackendService,
    private readonly session: SessionService,
    private readonly router: Router,
  ) {}

  entrar() {
    this.error = '';
    this.cargando = true;
    this.backend.login(this.correo, this.password).subscribe({
      next: (usuario) => {
        this.session.iniciar(usuario);
        this.router.navigate(['/dashboard']);
      },
      error: () => {
        this.cargando = false;
        this.error = 'Credenciales incorrectas';
      },
    });
  }
}