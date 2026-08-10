import React from "react";
import { Image, Pressable, Text, View } from "react-native";

import icons from "../assets/icons.js";

export default function BookingScreen({ slots, onHold }) {
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>Book a slot</Text>
      <Image source={icons.divider} style={styles.divider} />

      {slots.map((slot) => (
        <View key={slot.id} style={styles.row}>
          <Text style={styles.when}>{slot.when}</Text>
          <Text style={styles.who}>
            {slot.heldBy ? "Held by " + slot.heldBy : "Free"}
          </Text>
          <Pressable style={styles.hold} onPress={() => onHold(slot.id)}>
            <Text style={styles.holdLabel}>Hold</Text>
          </Pressable>
        </View>
      ))}
    </View>
  );
}

const styles = {
  screen: { flex: 1, padding: 16, gap: 8 },
  title: { fontSize: 24, fontWeight: "600" },
  divider: { height: 2, width: "100%", opacity: 0.3 },
  row: { flexDirection: "row", alignItems: "center", gap: 12 },
  when: { fontSize: 17, width: 88 },
  who: { flex: 1, fontSize: 14, opacity: 0.7 },
  hold: { paddingVertical: 8, paddingHorizontal: 16 },
  holdLabel: { fontSize: 15, fontWeight: "600" },
};
