<template>
  <div class="filter-tabs">
    <div class="mb-4">
      <h3 class="text-xs font-black text-fenix-gray-500 mb-3 uppercase tracking-[0.2em]">Género</h3>
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="option in genderOptions"
          :key="option.value"
          @click="$emit('update:gender', option.value)"
          class="tab-button"
          :class="selectedGender === option.value ? 'tab-active' : 'tab-inactive'"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'FilterTabs',
  props: {
    selectedGender: {
      type: String,
      default: null
    }
  },
  emits: ['update:gender'],
  data() {
    return {
      genderOptions: [
        { value: null, label: 'Todos' },
        { value: 'M', label: 'Hombres' },
        { value: 'F', label: 'Mujeres' }
      ]
    }
  }
}
</script>
