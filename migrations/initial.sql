CREATE TABLE "movimientos" (
	"id"	INTEGER,
	"date"	TEXT,
	"time"	TEXT,
	"moneda_from"	TEXT,
	"cantidad_from"	REAL,
	"moneda_to"	TEXT,
	"cantidad_to"	REAL,
	"preciounitario"	REAL,
	PRIMARY KEY("id")
)