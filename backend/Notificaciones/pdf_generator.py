from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _formato_cop(valor: int) -> str:
    return f"$ {valor:,.0f}".replace(",", ".")


def _fecha(año, mes, dia) -> str:
    return f"{dia:02d}/{mes:02d}/{año}"


def generar_pdf_estado_cuenta(cliente, facturas, link_portal=None) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        title=f"Estado de cuenta - {cliente.nombre_empresa}",
        author="PruebaOsa",
    )

    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle("Titulo", parent=estilos["Title"], fontSize=16, spaceAfter=2 * mm)
    subtitulo = ParagraphStyle("Subtitulo", parent=estilos["Normal"], textColor=colors.grey, fontSize=9)
    celda = ParagraphStyle("Celda", parent=estilos["Normal"], fontSize=8, leading=10)
    celda_der = ParagraphStyle("CeldaDer", parent=celda, alignment=TA_RIGHT)
    cabecera = ParagraphStyle("Cabecera", parent=celda, textColor=colors.white, fontName="Helvetica-Bold")
    cabecera_der = ParagraphStyle("CabeceraDer", parent=cabecera, alignment=TA_RIGHT)
    nota = ParagraphStyle("Nota", parent=estilos["Normal"], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)

    elementos = [
        Paragraph(f"Estado de cuenta", titulo),
        Paragraph(f"{cliente.nombre_empresa} · NIT {cliente.nit}", subtitulo),
        Spacer(1, 2 * mm),
    ]

    total = sum(f["valor"] for f in facturas)
    filas = [
        [
            Paragraph("Factura", cabecera),
            Paragraph("Vencimiento", cabecera),
            Paragraph("Días de mora", cabecera),
            Paragraph("Valor (COP)", cabecera_der),
            Paragraph("Estado", cabecera),
        ]
    ]
    for f in facturas:
        filas.append(
            [
                Paragraph(f["numero_factura"], celda),
                Paragraph(_fecha(*f["fecha_vencimiento"].timetuple()[:3]), celda),
                Paragraph(str(f["dias_mora"]), celda),
                Paragraph(_formato_cop(f["valor"]), celda_der),
                Paragraph(f["estado"], celda),
            ]
        )

    tabla = Table(filas, colWidths=[32 * mm, 30 * mm, 26 * mm, 40 * mm, 24 * mm], repeatRows=1)
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c7be5")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elementos.append(tabla)
    elementos.append(Spacer(1, 3 * mm))

    resumen = Table(
        [
            [Paragraph("Total pendiente", celda), Paragraph(_formato_cop(total), ParagraphStyle("Total", parent=celda, fontName="Helvetica-Bold", fontSize=11, alignment=TA_RIGHT))]
        ],
        colWidths=[60 * mm, 92 * mm],
    )
    resumen.setStyle(
        TableStyle(
            [
                ("LINEABOVE", (0, 0), (-1, 0), 1, colors.black),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elementos.append(resumen)
    elementos.append(Spacer(1, 8 * mm))

    if link_portal:
        elementos.append(
            Paragraph(
                f'Para ver el detalle actualizado en tiempo real, ingresa a: {link_portal}',
                nota,
            )
        )

    doc.build(elementos)
    buffer.seek(0)
    return buffer