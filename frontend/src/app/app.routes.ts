import { Routes } from '@angular/router';
import { canActivateAuth } from './services/auth.guard';
import { Login } from './login/login';
import { Dashboard } from './dashboard/dashboard';
import { EstadoCuenta } from './estado-cuenta/estado-cuenta';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'dashboard', component: Dashboard, canActivate: [canActivateAuth] },
  { path: 'estado-cuenta/:token', component: EstadoCuenta },
  { path: '**', redirectTo: '/login' },
];