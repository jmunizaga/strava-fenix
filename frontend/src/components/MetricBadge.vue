<template>
  <div class="metric-badge inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-fenix-gray-100 border border-fenix-gray-200 shadow-sm">
    <span class="text-xl">{{ icon }}</span>
    <div class="flex flex-col">
      <span class="text-[9px] font-black text-fenix-gray-400 uppercase tracking-wider">{{ label }}</span>
      <span class="text-xs font-black text-fenix-black tracking-tight">{{ formattedValue }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MetricBadge',
  props: {
    icon: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    value: {
      type: Number,
      required: true
    },
    unit: {
      type: String,
      default: ''
    },
    decimals: {
      type: Number,
      default: 1
    }
  },
  computed: {
    formattedValue() {
      const val = this.value.toFixed(this.decimals);
      return `${val} ${this.unit}`;
    }
  }
}
</script>
