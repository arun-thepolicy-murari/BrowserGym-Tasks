/**
 * BrowserGym Annotation — results recorder (Google Apps Script Web App)
 * ---------------------------------------------------------------------
 * Appends annotation submissions from the platform to three tabs of a
 * results spreadsheet: Tasks, Models, Steps. Headers are auto-created and
 * grow automatically as new columns appear — no schema to maintain.
 *
 * ── SETUP (do this exactly) ──────────────────────────────────────────
 * 1. Create a NEW Google Sheet (your results database). Copy its ID from
 *    the URL:  docs.google.com/spreadsheets/d/<THIS_IS_THE_ID>/edit
 * 2. Paste that ID into SHEET_ID below (between the quotes).
 * 3. Extensions ▸ Apps Script. Delete the stub, paste this whole file, Save.
 * 4. Run the function `setup` once (pick it in the toolbar ▸ Run) and click
 *    "Review permissions" ▸ allow. This proves the ID + access work and
 *    creates the three tabs.
 * 5. Deploy ▸ New deployment ▸ type "Web app".
 *        Execute as:        Me
 *        Who has access:    Anyone            ← MUST be "Anyone"
 *    Deploy, copy the Web app URL (…/exec).
 * 6. In the platform: ⚙ ▸ paste URL ▸ Save ▸ Test. A TEST row appears in Tasks.
 *
 * ── AFTER ANY CODE EDIT ──────────────────────────────────────────────
 * Deploy ▸ Manage deployments ▸ (edit, pencil) ▸ Version: "New version" ▸
 * Deploy. The URL stays the same but now serves your new code. Editing the
 * code WITHOUT a new version does nothing to the live URL.
 *
 * Quick self-test: open the /exec URL in a browser. You should see JSON
 * like {"ok":true,...}. If you see a Google sign-in page, access is not
 * "Anyone" — fix step 5.
 */

// ▼▼▼ PASTE YOUR RESULTS SPREADSHEET ID HERE ▼▼▼
var SHEET_ID = "PASTE_YOUR_SPREADSHEET_ID_HERE";
// ▲▲▲ (leave as-is only if you bound this script from inside the sheet) ▲▲▲

function book_() {
  // Prefer the explicit ID (works for standalone scripts). Fall back to the
  // bound spreadsheet if you created the script from Extensions ▸ Apps Script.
  if (SHEET_ID && SHEET_ID.indexOf("PASTE_") !== 0) {
    return SpreadsheetApp.openById(SHEET_ID);
  }
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error("No SHEET_ID set and script is not bound to a spreadsheet.");
  return ss;
}

function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    var ss = book_();
    var counts = {};
    // Current format: one wide row per task -> "Annotations" tab.
    if (payload.annotations) counts.Annotations = appendRows_(ss, "Annotations", payload.annotations);
    // Backward-compatible (older 3-sheet format), harmless if unused.
    if (payload.task)   counts.Tasks  = appendRows_(ss, "Tasks",  payload.task);
    if (payload.models) counts.Models = appendRows_(ss, "Models", payload.models);
    if (payload.steps)  counts.Steps  = appendRows_(ss, "Steps",  payload.steps);
    return json_({ ok: true, appended: counts });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

// GET = health check. Open the /exec URL in a browser to see this.
function doGet() {
  try {
    var ss = book_();
    return json_({ ok: true, service: "browsergym-annotation-recorder", spreadsheet: ss.getName() });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

// Run this ONCE from the editor to authorize + create the tabs.
function setup() {
  var ss = book_();
  if (!ss.getSheetByName("Annotations")) ss.insertSheet("Annotations");
  Logger.log("OK — using spreadsheet: " + ss.getName());
}

function appendRows_(ss, sheetName, rows) {
  if (!rows || !rows.length) return 0;
  var sheet = ss.getSheetByName(sheetName) || ss.insertSheet(sheetName);

  var header = sheet.getLastRow() > 0
    ? sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0].filter(String)
    : [];
  rows.forEach(function (r) {
    Object.keys(r).forEach(function (k) { if (header.indexOf(k) === -1) header.push(k); });
  });

  sheet.getRange(1, 1, 1, header.length).setValues([header]);
  sheet.getRange(1, 1, 1, header.length).setFontWeight("bold");
  sheet.setFrozenRows(1);

  var matrix = rows.map(function (r) {
    return header.map(function (k) {
      var v = r[k];
      return (v === undefined || v === null) ? "" : v;
    });
  });
  sheet.getRange(sheet.getLastRow() + 1, 1, matrix.length, header.length).setValues(matrix);
  return matrix.length;
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
