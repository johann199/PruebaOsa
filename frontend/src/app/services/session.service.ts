import { Injectable, signal } from '@angular/core';

export interface Usuario {
  id: number;
  nombre: string;
  rol: string;
  correo: string;
}

const STORAGE_KEY = 'cartera_usuario';

@Injectable({ providedIn: 'root' })
export class SessionService {
  readonly usuario = signal<Usuario | null>(this.cargar());

  private cargar(): Usuario | null {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? (JSON.parse(raw) as Usuario) : null;
    } catch {
      return null;
    }
  }

  iniciar(usuario: Usuario) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(usuario));
    this.usuario.set(usuario);
  }

  cerrar() {
    localStorage.removeItem(STORAGE_KEY);
    this.usuario.set(null);
  }

  estaAutenticado(): boolean {
    return this.usuario() !== null;
  }
}