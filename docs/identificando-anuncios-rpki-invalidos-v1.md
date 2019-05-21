# IDENTIFICAR ORGIDS CON ANUNCIOS ROA INVÁLIDOS

**Autor: carlos@lacnic.net en Punta Cana**
**Fecha: 5 de mayo de 2019**

## Objetivo:

Identificar las organizaciones asociadas a LACNIC que están realizando anuncios de recursos en Internet vía BGP que actualmente serían invalidados por un router que implementara “*routing origin validation*”.

## Descripción del pipeline:

El pipeline consta de 4 pasos y sería así:

- bajar la ultima version del netdata
- generar el netdata.db (esto tiene su propio pipeline)
- - *script: s0_get_netdatadb*
  - *salida: netdata-latest.db*

- generar la lista de prefijos invalidados

- - *script: s1_invalid_prefixes*

  - *salida: s1_invalid_prefixes.csv*

  - - *formato:*  ```Prefix|Status|OriginAS|ROAAS|ROAPrefix|MaxLen```

- agregarle a cada línea el org-id:

- - *script: s2_enrich_with_orgid*

  - *salida: s2_enrich_with_orgid.csv*

  - - *format:*  ```Prefix|Status|OriginAS|ROAAS|ROAPrefix|MaxLen|ORGID```

- agrupar listado por org ids y generar un segundo listado por org ids con número de anuncios invalidados

- - *script: s3_group_by_orgid*



## Publicación de resultados:

Los productos de este pipeline son:

*TBW

Están disponibles en:

*TBA