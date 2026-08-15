-- Run with: osascript scripts/export-pdf.applescript input.docx output.pdf
-- Microsoft Word must be installed. This release step is intentionally manual.
on run argv
  if (count of argv) is not 2 then error "Usage: input.docx output.pdf"
  set inputFile to POSIX file (item 1 of argv)
  set outputFile to POSIX file (item 2 of argv)
  tell application "Microsoft Word"
    activate
    set documentRef to open inputFile
    save as documentRef file name outputFile file format format PDF
    close documentRef saving no
  end tell
end run
