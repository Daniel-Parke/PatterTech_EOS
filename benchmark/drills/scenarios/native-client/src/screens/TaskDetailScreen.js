import React, { useState } from "react";
import { Pressable, Text, TextInput, View } from "react-native";

export default function TaskDetailScreen({ task, onSaveNote, onBack }) {
  const [draft, setDraft] = useState("");

  return (
    <View style={styles.screen}>
      <Pressable onPress={onBack} accessibilityRole="button"
                 accessibilityLabel="Back to the task list">
        <Text style={styles.back}>Back</Text>
      </Pressable>

      <Text style={styles.title}>{task.title}</Text>

      <Text style={styles.note}>{noteText(task)}</Text>

      <TextInput
        style={styles.input}
        value={draft}
        onChangeText={setDraft}
        placeholder="Add a note"
        multiline
      />

      <Pressable style={styles.save} onPress={() => onSaveNote(draft)}>
        <Text style={styles.saveLabel}>Save</Text>
      </Pressable>
    </View>
  );
}

function noteText(task) {
  const segments = (task.note && task.note.segments) || [];
  return segments.map((segment) => segment.text).join(" ");
}

const styles = {
  screen: { flex: 1, padding: 16, gap: 12 },
  back: { fontSize: 15 },
  title: { fontSize: 24, fontWeight: "600" },
  note: { fontSize: 16, lineHeight: 22 },
  input: { minHeight: 88, borderWidth: 1, borderRadius: 8, padding: 8 },
  save: { alignSelf: "flex-start", paddingVertical: 10, paddingHorizontal: 20 },
  saveLabel: { fontSize: 16, fontWeight: "600" },
};
