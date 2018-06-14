export const conditions = {
  "Digital Outputs": {
    checks: {
      "Equal To": {
        input: "select",
        options: ["High", "Low"]
      }
    },
    checksOptions: ["Equal To"],
    actions: {
      "Set Value": {
        input: "select",
        options: ["High", "Low"]
      },
      Toggle: {
        input: "N/A"
      }
    },
    actionsOptions: ["Set Value", "Toggle"]
  },
  "Digital Inputs": {
    checks: {
      "Equal To": {
        input: "select",
        options: ["Pressed", "Released", "Held Down", "Held Up"]
      }
    },
    checksOptions: ["Equal To"],
    actions: {},
    actionsOptions: []
  },
  "Analog Inputs": {
    checks: {
      "Greater Than": {
        input: "number",
        min: 0,
        max: 1023
      },
      "Less Than": {
        input: "number",
        min: 0,
        max: 1023
      },
      "Equal To": {
        input: "number",
        min: 0,
        max: 1023
      }
    },
    checksOptions: ["Greater Than", "Less Than", "Equal To"],
    actions: {},
    actionsOptions: []
  },
  Timers: {
    checks: {
      "Greater Than": {
        input: "timer"
      },

      "Less Than": {
        input: "timer"
      },

      "Equal To": {
        input: "timer"
      },
      "Get State": {
        input: "select",
        options: ["Running", "Paused", "Stopped"]
      }
    },
    checksOptions: ["Greater Than", "Less Than", "Equal To", "Get State"],
    actions: {
      "Set Value": {
        input: "timer"
      },
      "Set State": {
        input: "select",
        options: ["Run", "Pause", "Stop"]
      }
    },
    actionsOptions: ["Set Value", "Set State"]
  },
  Counters: {
    checks: {
      "Greater Than": {
        input: "number"
      },

      "Less Than": {
        input: "number"
      },

      "Equal To": {
        input: "number"
      }
    },
    checksOptions: ["Greater Than", "Less Than", "Equal To"],
    actions: {
      "Set Value": {
        input: "number"
      },
      "Increase Count": {
        input: "number"
      },
      "Decrease Count": {
        input: "number"
      }
    },
    actionsOptions: ["Set Value", "Increase Count", "Decrease Count"]
  },
  "Video Player": {
    checks: {},
    checksOptions: [],
    actions: {
      Play: {
        input: "N/A"
      },
      Stop: {
        input: "N/A"
      }
    },
    actionsOptions: ["Play", "Stop"]
  },
  "Audio Player": {
    checks: {},
    checksOptions: [],
    actions: {
      Play: {
        input: "N/A"
      },
      Stop: {
        input: "N/A"
      }
    },
    actionsOptions: ["Play", "Stop"]
  }
};
