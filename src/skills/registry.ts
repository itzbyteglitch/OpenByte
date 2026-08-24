import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";
import type { Skill } from "../core/types.js";

export class SkillRegistry {
  async discover(roots: string[]): Promise<Skill[]> {
    const skills: Skill[] = [];

    for (const root of roots) {
      let entries;
      try {
        entries = await readdir(root, { withFileTypes: true });
      } catch {
        continue;
      }

      for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        const skillFile = join(root, entry.name, "SKILL.md");
        try {
          const instructions = await readFile(skillFile, "utf8");
          const description = instructions.split("\n").find((line) => line.trim()) ?? entry.name;
          skills.push({
            name: entry.name,
            description,
            path: join(root, entry.name),
            instructions,
          });
        } catch {
          // Ignore directories that are not Skills.
        }
      }
    }

    return skills;
  }
}
