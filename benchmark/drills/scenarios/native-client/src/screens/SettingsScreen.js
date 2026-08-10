import React from "react";
import { Switch, Text, View } from "react-native";

export default function SettingsScreen({ preferences, onChange }) {
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Settings</Text>

      <View style={styles.row}>
        <Text style={styles.label}>Dark theme</Text>
        <Switch
          value={preferences.theme === "dark"}
          onValueChange={(on) => onChange("theme", on ? "dark" : "light")}
        />
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Remind me the evening before</Text>
        <Switch
          value={preferences.reminder === "evening"}
          onValueChange={(on) =>
            onChange("reminder", on ? "evening" : "morning")}
          accessibilityLabel="Remind me the evening before"
        />
      </View>
    </View>
  );
}

const styles = {
  screen: { flex: 1, padding: 16, gap: 16 },
  title: { fontSize: 24, fontWeight: "600" },
  row: { flexDirection: "row", alignItems: "center", justifyContent:
    "space-between" },
  label: { fontSize: 16 },
};
