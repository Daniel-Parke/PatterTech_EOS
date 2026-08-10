-- Undo for 0002. Run by hand against the primary if the release has to
-- be pulled, then redeploy the previous image.

ALTER TABLE users DROP COLUMN signup_source;
