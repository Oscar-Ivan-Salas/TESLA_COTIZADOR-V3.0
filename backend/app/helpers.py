"""
Funciones auxiliares generales
"""
import re
import unicodedata
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# ============================================
# FORMATEO DE TEXTO
# ============================================

def generar_slug(texto: str) -> str:
    """
    Generar slug URL-friendly desde texto
    
    Args:
        texto: Texto a convertir
    
    Returns:
        Slug en minúsculas, sin espacios ni caracteres especiales
    
    Ejemplo:
        generar_slug("Cotización #123 - Tesla Motors") -> "cotizacion-123-tesla-motors"
    """
    
    # Normalizar caracteres unicode (quitar acentos)
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Reemplazar espacios y caracteres especiales por guiones
    texto = re.sub(r'[^a-z0-9]+', '-', texto)
    
    # Eliminar guiones al inicio y final
    texto = texto.strip('-')
    
    # Eliminar guiones múltiples
    texto = re.sub(r'-+', '-', texto)
    
    return texto

def limpiar_texto(texto: str) -> str:
    """
    Limpiar texto eliminando espacios múltiples y caracteres extraños
    
    Args:
        texto: Texto a limpiar
    
    Returns:
        Texto limpio
    """
    
    if not texto:
        return ""
    
    # Eliminar espacios múltiples
    texto = " ".join(texto.split())
    
    # Eliminar saltos de línea múltiples
    texto = re.sub(r'\n+', '\n', texto)
    
    # Eliminar caracteres de control
    texto = ''.join(char for char in texto if unicodedata.category(char)[0] != 'C' or char in '\n\t')
    
    return texto.strip()

def extraer_numeros(texto: str) -> List[float]:
    """
    Extraer todos los números de un texto
    
    Args:
        texto: Texto del cual extraer números
    
    Returns:
        Lista de números encontrados
    
    Ejemplo:
        extraer_numeros("Precio: S/ 1,500.50 + IGV 270.09") -> [1500.50, 270.09]
    """
    
    # Patrón para números (enteros y decimales)
    patron = r'\d+(?:,\d{3})*(?:\.\d+)?'
    
    numeros_texto = re.findall(patron, texto)
    
    # Convertir a float (eliminar comas de miles)
    numeros = []
    for num_str in numeros_texto:
        try:
            num_limpio = num_str.replace(',', '')
            numeros.append(float(num_limpio))
        except ValueError:
            continue
    
    return numeros

# ============================================
# FORMATEO DE MONEDA
# ============================================

def formatear_moneda(
    monto: float,
    simbolo: str = "S/",
    decimales: int = 2
) -> str:
    """
    Formatear número como moneda
    
    Args:
        monto: Cantidad a formatear
        simbolo: Símbolo de moneda
        decimales: Número de decimales
    
    Returns:
        Texto formateado
    
    Ejemplo:
        formatear_moneda(1500.50) -> "S/ 1,500.50"
    """
    
    try:
        # Formatear con comas de miles
        monto_formateado = f"{monto:,.{decimales}f}"
        
        return f"{simbolo} {monto_formateado}"
        
    except Exception as e:
        logger.error(f"Error al formatear moneda: {str(e)}")
        return f"{simbolo} 0.00"

def calcular_igv(
    subtotal: float,
    porcentaje: float = 18.0
) -> tuple[float, float]:
    """
    Calcular IGV y total
    
    Args:
        subtotal: Monto base
        porcentaje: Porcentaje de IGV (default 18%)
    
    Returns:
        Tupla (igv, total)
    
    Ejemplo:
        calcular_igv(1000) -> (180.0, 1180.0)
    """
    
    try:
        igv = round(subtotal * (porcentaje / 100), 2)
        total = round(subtotal + igv, 2)
        
        return igv, total
        
    except Exception as e:
        logger.error(f"Error al calcular IGV: {str(e)}")
        return 0.0, subtotal

# ============================================
# VALIDACIONES
# ============================================

def validar_ruc(ruc: str) -> bool:
    """
    Validar RUC peruano
    
    Args:
        ruc: Número de RUC (11 dígitos)
    
    Returns:
        True si es válido
    """
    
    # Limpiar espacios
    ruc = ruc.strip()
    
    # Debe tener 11 dígitos
    if not re.match(r'^\d{11}$', ruc):
        return False
    
    # Debe empezar con 10, 15, 16, 17, o 20
    if not ruc.startswith(('10', '15', '16', '17', '20')):
        return False
    
    # Algoritmo de validación de RUC
    try:
        factores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        suma = sum(int(ruc[i]) * factores[i] for i in range(10))
        
        resto = suma % 11
        digito_verificador = 11 - resto
        
        if digito_verificador == 10:
            digito_verificador = 0
        elif digito_verificador == 11:
            digito_verificador = 1
        
        return digito_verificador == int(ruc[10])
        
    except Exception as e:
        logger.error(f"Error al validar RUC: {str(e)}")
        return False

def validar_email(email: str) -> bool:
    """
    Validar formato de email
    
    Args:
        email: Email a validar
    
    Returns:
        True si es válido
    """
    
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(patron, email))

def validar_telefono_peru(telefono: str) -> bool:
    """
    Validar número de teléfono peruano
    
    Args:
        telefono: Número de teléfono
    
    Returns:
        True si es válido
    """
    
    # Limpiar espacios y caracteres
    telefono = re.sub(r'[^0-9+]', '', telefono)
    
    # Celular: 9 dígitos empezando con 9
    # Fijo Lima: 7 dígitos
    # Con código país: +51 seguido de 9 dígitos
    
    patrones = [
        r'^9\d{8}$',           # Celular
        r'^\d{7}$',            # Fijo Lima
        r'^\+519\d{8}$',       # Celular con código país
        r'^\+51\d{7}$'         # Fijo con código país
    ]
    
    return any(re.match(patron, telefono) for patron in patrones)

# ============================================
# FECHAS
# ============================================

def fecha_actual() -> str:
    """
    Obtener fecha actual en formato ISO
    
    Returns:
        Fecha en formato YYYY-MM-DD
    """
    
    return datetime.now().strftime('%Y-%m-%d')

def fecha_formato_largo(fecha: Optional[datetime] = None) -> str:
    """
    Formatear fecha en formato largo en español
    
    Args:
        fecha: Fecha a formatear (default: hoy)
    
    Returns:
        Fecha formateada
    
    Ejemplo:
        fecha_formato_largo() -> "18 de octubre de 2025"
    """
    
    if not fecha:
        fecha = datetime.now()
    
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    dia = fecha.day
    mes = meses[fecha.month]
    anio = fecha.year
    
    return f"{dia} de {mes} de {anio}"

def parsear_fecha(texto_fecha: str) -> Optional[datetime]:
    """
    Parsear fecha desde texto en varios formatos
    
    Args:
        texto_fecha: Texto con fecha
    
    Returns:
        Objeto datetime o None si no se puede parsear
    """
    
    formatos = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%d/%m/%y',
        '%d-%m-%y'
    ]
    
    for formato in formatos:
        try:
            return datetime.strptime(texto_fecha, formato)
        except ValueError:
            continue
    
    return None

# ============================================
# ARCHIVOS
# ============================================

def obtener_extension(nombre_archivo: str) -> str:
    """
    Obtener extensión de archivo
    
    Args:
        nombre_archivo: Nombre del archivo
    
    Returns:
        Extensión sin punto (en minúsculas)
    """
    
    from pathlib import Path
    
    extension = Path(nombre_archivo).suffix.lower()
    
    return extension.replace('.', '')

def formatear_tamano_archivo(bytes: int) -> str:
    """
    Formatear tamaño de archivo en formato legible
    
    Args:
        bytes: Tamaño en bytes
    
    Returns:
        Tamaño formateado
    
    Ejemplo:
        formatear_tamano_archivo(1500000) -> "1.43 MB"
    """
    
    if bytes < 1024:
        return f"{bytes} bytes"
    elif bytes < 1024 ** 2:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1024 ** 3:
        return f"{bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{bytes / (1024 ** 3):.2f} GB"

# ============================================
# NÚMEROS
# ============================================

def numero_a_texto(numero: int) -> str:
    """
    Convertir número a texto en español (1-999)
    
    Args:
        numero: Número a convertir
    
    Returns:
        Número en texto
    
    Ejemplo:
        numero_a_texto(123) -> "ciento veintitrés"
    """
    
    unidades = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']
    decenas = ['', 'diez', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']
    especiales = {
        11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce', 15: 'quince',
        16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho', 19: 'diecinueve'
    }
    centenas = ['', 'ciento', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos',
                'seiscientos', 'setecientos', 'ochocientos', 'novecientos']
    
    if numero == 0:
        return 'cero'
    
    if numero < 0 or numero > 999:
        return str(numero)
    
    resultado = []
    
    # Centenas
    if numero >= 100:
        if numero == 100:
            return 'cien'
        resultado.append(centenas[numero // 100])
        numero %= 100
    
    # Decenas y unidades
    if numero >= 11 and numero <= 19:
        resultado.append(especiales[numero])
    elif numero >= 10:
        resultado.append(decenas[numero // 10])
        if numero % 10:
            if numero // 10 == 2:
                resultado[-1] = 'veinti' + unidades[numero % 10]
            else:
                resultado.append('y')
                resultado.append(unidades[numero % 10])
    elif numero > 0:
        resultado.append(unidades[numero])
    
    return ' '.join(resultado)

def redondear_decimal(valor: float, decimales: int = 2) -> Decimal:
    """
    Redondear número a Decimal con precisión
    
    Args:
        valor: Número a redondear
        decimales: Cantidad de decimales
    
    Returns:
        Decimal redondeado
    """
    
    from decimal import Decimal, ROUND_HALF_UP
    
    quantize_str = '0.' + '0' * decimales
    
    return Decimal(str(valor)).quantize(
        Decimal(quantize_str),
        rounding=ROUND_HALF_UP
    )