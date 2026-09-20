from ninja import Router
from datetime import date, timedelta
from django.db.models import Sum
from Factura.models import Factura

dashboard = Router()

@dashboard.get("/resumen")
def dashboard_gestor(request):
    hoy = date.today()
    facturas = Factura.objects.filter(estado__in=["Pendiente", "Vencida"]).select_related("cliente")

    prioridades = []
    proyeccion = {"30": 0, "60": 0, "90": 0, "mas_90": 0}

    for f in facturas:
        dias_mora = max((hoy - f.fecha_vencimiento).days, 0)
        promedio = f.cliente.promedio_dias_pago

        # Score de prioridad
        score = (dias_mora - promedio) * f.valor

        prioridades.append({
            "cliente": f.cliente.nombre_empresa,
            "factura": f.numero_factura,
            "dias_mora": dias_mora,
            "promedio_historico": promedio,
            "valor": f.valor,
            "score_prioridad": score,
        })

        # Proyección de recaudo
        fecha_estimada = f.fecha_vencimiento + timedelta(days=promedio)
        dias_restantes = (fecha_estimada - hoy).days

        if dias_restantes <= 30:
            proyeccion["30"] += f.valor
        elif dias_restantes <= 60:
            proyeccion["60"] += f.valor
        elif dias_restantes <= 90:
            proyeccion["90"] += f.valor
        else:
            proyeccion["mas_90"] += f.valor

    # Ordena de mayor a menor prioridad para el analista
    prioridades.sort(key=lambda x: x["score_prioridad"], reverse=True)

    return {
        "clientes_prioritarios": prioridades,
        "proyeccion_recaudo": proyeccion,
        "total_cartera": facturas.aggregate(total=Sum("valor"))["total"] or 0,
        "cantidad_facturas": facturas.count(),
    }