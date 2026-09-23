// Public catalog -> Excel. Requires the maintainer's bundled @oai/artifact-tool runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const [input, output, previewDir] = process.argv.slice(2);
if (!input || !output || !process.env.QA_COVERAGE_MODULES) {
  throw new Error('Usar qa.cmd coverage; faltan archivo fuente, destino o runtime.');
}
const resolveModule = createRequire(path.join(path.resolve(process.env.QA_COVERAGE_MODULES), '..', 'coverage.cjs'));
const { Workbook, SpreadsheetFile } = await import(pathToFileURL(resolveModule.resolve('@oai/artifact-tool')));
const raw = await fs.readFile(input, 'utf8');
const snapshot = JSON.parse(raw);
if (snapshot.schema_version !== 1) throw new Error('Versión de mapa no soportada.');
const xgestion = snapshot.products.find(product => product.id === 'xgestion');
if (!xgestion) throw new Error('Falta XGestión en el catálogo.');
// Other products appear only in the readiness table. Reused group IDs and future
// scenarios must not change XGestión's counts or labels.
const data = { ...snapshot,
  scenarios: snapshot.scenarios.filter(item => item.product === 'xgestion'),
  groups: snapshot.groups.filter(item => item.product === 'xgestion'),
  counts: { ...snapshot.counts, ...xgestion.counts,
    groups: snapshot.groups.filter(item => item.product === 'xgestion').length },
};
const wb = Workbook.create();
const names = ['Resumen', 'Grupos', 'Escenarios', 'Por detallar', 'Ejemplos seed'];
const sheets = Object.fromEntries(names.map(name => [name, wb.worksheets.add(name)]));
const navy = '#17324D', blue = '#245B89', ink = '#243746', pale = '#F0F5FA', amber = '#FFF0CC';
const status = { implemented: 'Automatizado', planned: 'Pendiente', manual: 'Manual' };
const groupNames = Object.fromEntries(data.groups.map(group => [group.id, group.title]));
const stageNames = Object.fromEntries(data.stages.map(stage => [stage.id, stage.title]));
const regions = [];
const col = index => String.fromCharCode(65 + index);
const literal = value => typeof value === 'string' && /^[=+@-]/.test(value) ? `'${value}` : value ?? '';
const text = value => typeof value === 'object' && value !== null ? `${value.label}\n${value.url}` : value;
const link = (url, label) => ({ url, label });
function caseList(ids) {
  const ranges = [];
  for (let index = 0; index < ids.length;) {
    const first = /^(.*?)(\d+)$/.exec(ids[index]);
    let end = index;
    while (first && end + 1 < ids.length) {
      const next = String(Number(first[2]) + end - index + 1).padStart(first[2].length, '0');
      if (ids[end + 1] !== first[1] + next) break;
      end += 1;
    }
    ranges.push(end > index ? `${ids[index]}..${ids[end].slice(first[1].length)}` : ids[index]);
    index = end + 1;
  }
  return Array.from({ length: Math.ceil(ranges.length / 3) },
    (_, index) => ranges.slice(index * 3, index * 3 + 3).join(', ')).join('\n');
}
function sourceLink(sheet, address, item) {
  if (!item.url.startsWith(data.repository_url + '/')) throw new Error('Referencia pública fuera del repositorio.');
  // HYPERLINK does not calculate in the bundled engine. Keep readable literal URLs,
  // without unsupported formula caches or links to local/private files.
  sheet.getRange(address).values = [[literal(text(item))]];
  sheet.getRange(address).format.font = { color: blue };
}
function base(sheet, title, note, widths, endRow) {
  const last = col(widths.length - 1);
  const area = sheet.getRange(`A1:${last}${endRow}`);
  area.format.font = { name: 'Arial', size: 11, color: ink };
  area.format.verticalAlignment = 'center';
  area.format.wrapText = true;
  widths.forEach((width, index) => { sheet.getRange(`${col(index)}1:${col(index)}${endRow}`).format.columnWidthPx = width; });
  sheet.showGridLines = false;
  sheet.tabColor = navy;
  sheet.getRange(`A1:${last}2`).format.fill = navy;
  sheet.getRange('A1').values = [[title]];
  sheet.getRange('A1').format.font = { name: 'Arial', size: 22, bold: true, color: '#FFFFFF' };
  sheet.getRange('A1').format.wrapText = false;
  sheet.getRange(`A1:${last}1`).format.rowHeightPx = 40;
  sheet.getRange(`A2:${last}2`).format.rowHeightPx = 8;
  sheet.mergeCells(`A3:${last}4`);
  sheet.getRange('A3').values = [[note]];
  sheet.getRange(`A3:${last}4`).format.fill = pale;
  sheet.getRange(`A3:${last}4`).format.rowHeightPx = 24;
  sheet.getRange(`A5:${last}5`).format.rowHeightPx = 14;
  sheet.freezePanes.freezeRows(6);
}
function header(sheet, range) {
  sheet.getRange(range).format = { fill: blue, font: { name: 'Arial', size: 11, color: '#FFFFFF', bold: true },
    rowHeightPx: 40, wrapText: true, verticalAlignment: 'center' };
}
function table(name, title, note, headings, rows, widths, tableName) {
  const sheet = sheets[name], last = col(headings.length - 1), end = rows.length + 6;
  base(sheet, title, note, widths, end);
  sheet.getRange(`A6:${last}${end}`).values = [headings, ...rows.map(row => row.map(value => literal(text(value))))];
  const grid = sheet.tables.add(`A6:${last}${end}`, true, tableName);
  grid.style = 'TableStyleMedium2';
  grid.showFilterButton = true;
  header(sheet, `A6:${last}6`);
  rows.forEach((row, index) => {
    const number = index + 7;
    const lines = Math.max(...row.map((item, column) => String(text(item) ?? '').split('\n')
      .reduce((sum, line) => sum + Math.max(1, Math.ceil(line.length / Math.max(12, (widths[column] - 18) / 8))), 0)));
    sheet.getRange(`A${number}:${last}${number}`).format.rowHeightPx = Math.max(54, lines * 18 + 18);
    if (index % 2 === 1) sheet.getRange(`A${number}:${last}${number}`).format.fill = pale;
    row.forEach((item, column) => { if (typeof item === 'object' && item !== null) sourceLink(sheet, `${col(column)}${number}`, item); });
  });
  regions.push({ sheetName: name, range: `A1:${last}${Math.min(end, 12)}`, end, last });
  return sheet;
}

const scenarios = table('Escenarios', 'Escenarios documentados',
  'Una fila por ID único. Automatizado significa que existe una prueba; la validación real sobre el JAR sigue pendiente. Prioridad heredada de la etapa.',
  ['ID', 'Recorrido del usuario', 'Automatización', 'Validación real', 'Etapa', 'Prioridad', 'Grupos para QA', 'Ficha', 'Prueba', 'Próximo paso'],
  data.scenarios.map(item => [item.id, item.title, status[item.status], 'Pendiente', item.stage, item.priority ?? 'Por definir',
    item.groups.map(id => `${groupNames[id]} [${id}]`).join('\n'), link(item.doc_url, 'Ver ficha'),
    item.test_url ? link(item.test_url, 'Ver prueba') : 'Sin automatizar',
    item.status === 'implemented' ? 'Calibrar y ejecutar sobre el JAR QA; registrar evidencia.' : 'Implementar la ficha y luego validar sobre el JAR QA.']),
  [140, 335, 125, 130, 65, 80, 360, 340, 340, 270], 'ScenariosTable');
scenarios.getRange(`C7:C${data.scenarios.length + 6}`).conditionalFormats.add('containsText',
  { text: 'Automatizado', format: { fill: '#DCEAF7', font: { color: blue, bold: true } } });
scenarios.getRange(`C7:D${data.scenarios.length + 6}`).conditionalFormats.add('containsText',
  { text: 'Pendiente', format: { fill: amber, font: { color: '#805400' } } });

table('Grupos', 'Grupos de ejecución para QA',
  'Los grupos se superponen: no sumar sus cantidades. “Parcial” indica automatización disponible, sin afirmar que estén cubiertas todas las variantes de esa familia.',
  ['Etapa', 'Grupo', 'Clave de ejecución', 'Qué permite revisar', 'Automatizados', 'Pendientes', 'Manuales', 'Situación', 'IDs incluidos (..: rango)'],
  data.groups.map(item => [item.stage, item.title, item.id, item.description, item.counts.implemented, item.counts.planned,
    item.counts.manual, { partial: 'Parcial: ejecutable', planned: 'Pendiente', manual: 'Manual', 'no-scenarios': 'Sin fichas' }[item.status],
    caseList(item.members) || 'Por detallar']), [60, 240, 170, 430, 115, 105, 85, 180, 450], 'GroupsTable');
sheets.Grupos.getRange(`E7:G${data.groups.length + 6}`).format.horizontalAlignment = 'center';

const backlog = [
  ...data.backlog.families.map(item => ['Mapa funcional', 'Varias', item.title, item.variants, item.source_status,
    'Por detallar / ampliar', link(item.doc_url, 'Ver matriz')]),
  ...data.backlog.roadmap_variants.map(item => ['Familia del roadmap', item.stage, item.title, item.variants,
    `${item.priority} · ${item.limits}`, 'Por detallar', link(item.doc_url, 'Ver roadmap')]),
  ...data.backlog.restobar.map(item => [`Restobar · ${item.id}`, item.stage, item.title, item.dependencies,
    item.priority, 'Ver fichas relacionadas', link(item.doc_url, 'Ver recorrido')]),
];
table('Por detallar', 'Familias y referencias del roadmap',
  'Estas familias y recorridos orientan el trabajo pendiente. Las tablas fuente se solapan: no sumar filas como casos E2E. R01–R20 se vinculan a fichas pendientes de automatización; no agregan casos al catálogo.',
  ['Tipo de referencia', 'Etapa', 'Funcionalidad / recorrido', 'Variantes y dependencias', 'Prioridad / límites / estado fuente', 'Siguiente trabajo', 'Referencia'],
  backlog, [175, 65, 370, 470, 430, 200, 340], 'BacklogTable');

table('Ejemplos seed', 'Productos, ofertas y listas: ejemplos',
  'Datos y resultados esperados. Los ejemplos vinculados tienen su estado de automatización en Escenario E2E. La validación real sigue pendiente; revisar el perfil y las condiciones de cada ficha.',
  ['Ejemplo', 'Productos × cantidades', 'Lista', 'Total esperado', 'Moneda', 'Validación real', 'Escenario E2E', 'Condiciones', 'Datos', 'Trazabilidad ERP'],
  data.seed_examples.map(item => [item.id, Object.entries(item.quantities).map(([code, quantity]) => `${code} × ${quantity}`).join('\n'),
    item.selected_list ?? 'Según perfil', Number(item.expected_total), item.currency, 'Pendiente',
    item.e2e_scenario ? link(item.e2e_doc_url, `${item.e2e_scenario} · ${status[item.e2e_status]}`) : 'Sin ficha',
    item.note ?? 'Ver condiciones del catálogo comercial.',
    link(item.doc_url, 'Ver ejemplo'), `${item.source}\nCommit: ${item.erp_commit}`]),
  [200, 290, 120, 125, 75, 150, 340, 420, 340, 440], 'SeedExamplesTable');
sheets['Ejemplos seed'].getRange(`D7:D${data.seed_examples.length + 6}`).setNumberFormat('#,##0.00');

const summary = sheets.Resumen;
base(summary, 'Mapa de cobertura · XGestión',
  'Control de alto nivel: qué está automatizado y qué falta. Consultá los detalles usando los filtros de las otras hojas. Este archivo no es un resultado de ejecución.',
  [360, 115, 590], 42);
summary.getRange('A6:C11').values = [
  ['Fichas de XGestión', 'Cantidad', 'Cómo interpretar el número'],
  ['Documentadas (IDs únicos)', null, 'Universo de fichas actuales; no representa todo el ERP.'],
  ['Automatizadas', null, 'Código de prueba disponible. Ejecución real pendiente.'],
  ['Pendientes de automatizar', null, 'Criterios escritos; todavía sin prueba ejecutable.'],
  ['Manuales', null, 'Fichas registradas como pruebas manuales.'],
  ['Validadas con evidencia pública', null, 'Sin evidencia real registrada en este mapa. No inferir aprobación.'],
];
header(summary, 'A6:C6');
const lastCase = data.scenarios.length + 6;
summary.getRange('B7:B11').formulas = [
  [`=COUNTA('Escenarios'!$A$7:$A$${lastCase})`],
  [`=COUNTIF('Escenarios'!$C$7:$C$${lastCase},"Automatizado")`],
  [`=COUNTIF('Escenarios'!$C$7:$C$${lastCase},"Pendiente")`],
  [`=COUNTIF('Escenarios'!$C$7:$C$${lastCase},"Manual")`],
  [`=COUNTIF('Escenarios'!$D$7:$D$${lastCase},"Validado")`],
];
summary.getRange('A7:C11').format.rowHeightPx = 42;
summary.getRange('B7:B11').format.font = { name: 'Arial', size: 22, bold: true, color: blue };
summary.getRange('B7:B11').setNumberFormat('0');
summary.getRange('A9:C9').format.fill = amber;
summary.getRange('A11:C11').format.fill = pale;
summary.getRange('A14:C18').values = [['Producto', 'Fichas', 'Disponibilidad'],
  ...data.products.map(item => [item.title, item.counts.documented,
    item.status === 'implemented' ? 'Primeros escenarios implementados; validación real pendiente.' : 'Preparado en el repositorio; automatización pendiente.'])];
header(summary, 'A14:C14');
summary.getRange('A15:C18').format.rowHeightPx = 36;
summary.getRange('A21:C28').values = [['Etapa de XGestión', 'Automatizados', 'Pendientes / manuales'],
  ...data.stages.map(item => { const selected = data.scenarios.filter(row => row.stage === item.id);
    return [`${item.id}. ${stageNames[item.id]}`, selected.filter(row => row.status === 'implemented').length,
      selected.length ? `${selected.filter(row => row.status === 'planned').length} pendientes · ${selected.filter(row => row.status === 'manual').length} manuales`
        : 'Sin fichas todavía: ver Por detallar.']; })];
header(summary, 'A21:C21');
summary.getRange('A22:C28').format.rowHeightPx = 40;
summary.getRange('B7:B28').format.horizontalAlignment = 'center';
const linkedExamples = data.seed_examples.filter(item => item.e2e_scenario).length;
const notes = [
  `${data.counts.groups} grupos de ejecución. Sus conteos se solapan; el total de fichas se cuenta una vez por ID.`,
  `${data.counts.backlog_restobar} referencias Restobar vinculadas a fichas. ${data.counts.seed_examples} ejemplos seed: ${linkedExamples} vinculados a fichas y ${data.counts.seed_examples - linkedExamples} sin ficha. No se suman al total.`,
  'Automatización: azul = implementada · ámbar = pendiente. “Validación real” requiere JAR, entorno y reporte de ejecución.',
  'Actualización: editar fichas, grupos o roadmap en el repositorio; ejecutar qa.cmd coverage y guardar los archivos generados juntos.',
  'No editar este Excel a mano: la regeneración reemplaza su contenido. Guía: docs/cobertura.md.',
  `Revisión de fuentes públicas: SHA256 ${createHash('sha256').update(raw).digest('hex').slice(0, 16)}. Sin datos privados.`,
];
notes.forEach((note, index) => {
  const row = index + 31;
  summary.mergeCells(`A${row}:C${row}`);
  summary.getRange(`A${row}`).values = [[note]];
  summary.getRange(`A${row}:C${row}`).format.rowHeightPx = 38;
  summary.getRange(`A${row}:C${row}`).format.fill = pale;
});
sourceLink(summary, 'A38', link(data.repository_url + '/blob/main/docs/cobertura.md', 'Guía de uso y actualización'));
summary.mergeCells('A38:C38');
summary.getRange('A38:C38').format.rowHeightPx = 50;
regions.unshift({ sheetName: 'Resumen', range: 'A1:C38', end: 38, last: 'C' });

wb.recalculate();
const observed = summary.getRange('B7:B11').values.map(row => row[0]);
const expected = ['documented', 'implemented', 'planned', 'manual', 'real_validated'].map(key => data.counts[key]);
if (JSON.stringify(observed) !== JSON.stringify(expected)) throw new Error(`Resumen inconsistente: ${JSON.stringify(observed)}`);
const inspection = await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',
  options: { useRegex: true, maxResults: 100 }, maxChars: 6000 });
if (previewDir) {
  await fs.mkdir(previewDir, { recursive: true });
  await fs.writeFile(path.join(previewDir, 'inspection.txt'), inspection.ndjson);
  for (const region of regions) {
    const preview = await wb.render({ sheetName: region.sheetName, range: region.range, scale: 1, format: 'png' });
    await fs.writeFile(path.join(previewDir, `${region.sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
}
const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(output);
await new Promise(resolve => process.stdout.write(
  JSON.stringify({ sheets: names, scenarioCount: data.scenarios.length, summary: observed }) + '\n', resolve));
