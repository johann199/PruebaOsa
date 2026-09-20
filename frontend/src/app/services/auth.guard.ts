import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { SessionService } from './session.service';

export function canActivateAuth() {
  const session = inject(SessionService);
  const router = inject(Router);
  if (!session.estaAutenticado()) {
    return router.createUrlTree(['/login']);
  }
  return true;
}