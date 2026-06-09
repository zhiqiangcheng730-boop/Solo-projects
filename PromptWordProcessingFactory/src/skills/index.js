import naturalize from './naturalize.js';
import deAify from './deAify.js';
import fluencyOptimize from './fluencyOptimize.js';

const skills = [naturalize, deAify, fluencyOptimize];

export function getAllSkills() {
  return skills;
}

export function getSkillById(id) {
  return skills.find((s) => s.id === id) || null;
}
