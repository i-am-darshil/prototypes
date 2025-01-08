import { createLogger, format, transports } from "winston";

export function getLogger(serviceName: string) {
  // Create the logger
  const logger = createLogger({
    level: "info", // Default logging level
    format: format.combine(
      format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
      format.errors({ stack: true }), // Include error stack traces
      format.splat(), // String interpolation
      format.json() // Log in JSON format
    ),
    defaultMeta: { service: serviceName },
    transports: [
      // Write logs to a file
      new transports.File({ filename: "logs/error.log", level: "error" }),
      new transports.File({ filename: "logs/combined.log" }),
    ],
  });

  logger.add(
    new transports.Console({
      format: format.combine(format.colorize(), format.simple()),
    })
  );

  return logger;
}
