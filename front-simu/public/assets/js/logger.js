export var loggerLevel = {
    "INFO": {
        name: "INFO",
        level: 1
    }, "WARNING": {
        name: "INFO",
        level: 2
    }, "ERROR": {
        name: "ERROR",
        level: 3
    }, "DEBUG": {
        name: "DEBUG",
        level: 4
    }
}

export class logger {

    constructor(level) {
        this.level = loggerLevel[level];
    }



}