<template>
  <div class="color-palette-editor">
    <el-card shadow="never">
      <template #header>
        <div class="flex-between">
          <h5>{{ $t('components.colorPalette.primaryColor') }}</h5>
          <el-button size="small" text @click="resetToPreset('default')">
            {{ $t('views.system.theme.restoreDefaults') }}
          </el-button>
        </div>
      </template>
      
      <div class="color-controls">
        <!-- 主色调设置 -->
        <div class="color-item">
          <label class="color-label">
            {{ $t('components.colorPalette.primary') }}
          </label>
          <div class="color-input-group">
            <el-color-picker 
              v-model="localColors.primary" 
              @change="handleColorChange"
              show-alpha
              :predefine="predefineColors"
            />
            <el-input 
              v-model="localColors.primary" 
              :placeholder="$t('components.colorPalette.colorPlaceholder')"
              class="color-text-input"
              @input="handleColorChange"
            />
          </div>
        </div>

        <!-- 辅助色设置 -->
        <div class="color-item">
          <label class="color-label">
            {{ $t('components.colorPalette.secondary') }}
          </label>
          <div class="color-input-group">
            <el-color-picker 
              v-model="localColors.secondary" 
              @change="handleColorChange"
              show-alpha
              :predefine="predefineColors"
            />
            <el-input 
              v-model="localColors.secondary" 
              :placeholder="$t('components.colorPalette.colorPlaceholder')"
              class="color-text-input"
              @input="handleColorChange"
            />
          </div>
        </div>

        <!-- 强调色设置 -->
        <div class="color-item">
          <label class="color-label">
            {{ $t('components.colorPalette.accent') }}
          </label>
          <div class="color-input-group">
            <el-color-picker 
              v-model="localColors.accent" 
              @change="handleColorChange"
              show-alpha
              :predefine="predefineColors"
            />
            <el-input 
              v-model="localColors.accent" 
              :placeholder="$t('components.colorPalette.colorPlaceholder')"
              class="color-text-input"
              @input="handleColorChange"
            />
          </div>
        </div>
      </div>

      <!-- 预设配色方案 -->
      <div class="preset-colors">
        <h6 class="preset-title">{{ $t('components.colorPalette.presetColors') }}</h6>
        <div class="preset-grid">
          <div 
            v-for="(preset, key) in colorPresets" 
            :key="key"
            class="preset-item"
            :class="{ active: isActivePreset(preset) }"
            @click="applyPreset(preset)"
          >
            <div class="preset-colors">
              <div 
                class="preset-color" 
                :style="{ backgroundColor: preset.primary }"
              ></div>
              <div 
                class="preset-color" 
                :style="{ backgroundColor: preset.secondary }"
              ></div>
              <div 
                class="preset-color" 
                :style="{ backgroundColor: preset.accent }"
              ></div>
            </div>
            <span class="preset-name">{{ $t(`components.colorPalette.presets.${key}`) }}</span>
          </div>
        </div>
      </div>

      <!-- 颜色预览 -->
      <div class="color-preview">
        <h6 class="preview-title">{{ $t('components.colorPalette.preview') }}</h6>
        <div class="preview-content">
          <div class="preview-buttons">
            <el-button type="primary" :style="getPreviewStyle('primary')">
              {{ $t('components.colorPalette.primary') }}
            </el-button>
            <el-button :style="getPreviewStyle('secondary')">
              {{ $t('components.colorPalette.secondary') }}
            </el-button>
            <el-button type="success" :style="getPreviewStyle('accent')">
              {{ $t('components.colorPalette.accent') }}
            </el-button>
          </div>
          
          <div class="gradient-preview">
            <div 
              class="gradient-bar"
              :style="{
                background: `linear-gradient(135deg, ${localColors.primary}, ${localColors.secondary})`
              }"
            ></div>
            <span class="gradient-label">{{ $t('components.colorPalette.gradientPreview') }}</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, watch, computed } from 'vue'
import { t } from '@/locales'

defineOptions({
  name: 'ColorPaletteEditor'
})

interface ColorScheme {
  primary: string
  secondary: string
  accent: string
}

interface Props {
  modelValue: ColorScheme
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => ({
    primary: '#3370FF',
    secondary: '#6B7280',
    accent: '#10B981'
  })
})

const emit = defineEmits<{
  'update:modelValue': [value: ColorScheme]
  'change': [value: ColorScheme]
}>()

// 本地颜色状态
const localColors = reactive<ColorScheme>({
  primary: props.modelValue.primary,
  secondary: props.modelValue.secondary,
  accent: props.modelValue.accent
})

// 预设颜色
const predefineColors = ref([
  '#3370FF', '#FF8800', '#00B69D', '#7F3BF5', '#F01D94',
  '#1890FF', '#52C41A', '#FAAD14', '#F5222D', '#722ED1'
])

// 预设配色方案
const colorPresets = {
  default: {
    primary: '#3370FF',
    secondary: '#6B7280', 
    accent: '#10B981'
  },
  orange: {
    primary: '#FF8800',
    secondary: '#8B5CF6',
    accent: '#F59E0B'
  },
  green: {
    primary: '#00B69D',
    secondary: '#6B7280',
    accent: '#34D399'
  },
  purple: {
    primary: '#7F3BF5',
    secondary: '#A78BFA',
    accent: '#C084FC'
  },
  red: {
    primary: '#F01D94',
    secondary: '#F87171',
    accent: '#FB7185'
  },
  blue: {
    primary: '#1E40AF',
    secondary: '#3B82F6',
    accent: '#60A5FA'
  }
}

// 监听props变化
watch(() => props.modelValue, (newValue) => {
  Object.assign(localColors, newValue)
}, { deep: true })

// 处理颜色变化
const handleColorChange = () => {
  const colorScheme = { ...localColors }
  emit('update:modelValue', colorScheme)
  emit('change', colorScheme)
}

// 应用预设配色
const applyPreset = (preset: ColorScheme) => {
  Object.assign(localColors, preset)
  handleColorChange()
}

// 重置为默认配色
const resetToPreset = (presetKey: string) => {
  const preset = colorPresets[presetKey as keyof typeof colorPresets]
  if (preset) {
    applyPreset(preset)
  }
}

// 检查是否为当前激活的预设
const isActivePreset = (preset: ColorScheme) => {
  return localColors.primary === preset.primary &&
         localColors.secondary === preset.secondary &&
         localColors.accent === preset.accent
}

// 获取预览样式
const getPreviewStyle = (type: keyof ColorScheme) => {
  const color = localColors[type]
  return {
    backgroundColor: color,
    borderColor: color,
    color: '#ffffff'
  }
}
</script>

<style lang="scss" scoped>
.color-palette-editor {
  .color-controls {
    margin-bottom: 24px;

    .color-item {
      display: flex;
      align-items: center;
      margin-bottom: 16px;

      .color-label {
        min-width: 60px;
        margin-right: 12px;
        font-size: 14px;
        color: var(--el-text-color-regular);
      }

      .color-input-group {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 8px;

        .color-text-input {
          width: 120px;
        }
      }
    }
  }

  .preset-colors {
    margin-bottom: 24px;

    .preset-title {
      margin: 0 0 12px 0;
      font-size: 14px;
      font-weight: 500;
      color: var(--el-text-color-primary);
    }

    .preset-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
      gap: 12px;

      .preset-item {
        padding: 8px;
        border: 2px solid var(--el-border-color-light);
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;

        &:hover {
          border-color: var(--el-color-primary);
        }

        &.active {
          border-color: var(--el-color-primary);
          background-color: var(--el-color-primary-light-9);
        }

        .preset-colors {
          display: flex;
          justify-content: center;
          margin-bottom: 6px;

          .preset-color {
            width: 16px;
            height: 16px;
            border-radius: 2px;
            margin: 0 2px;
          }
        }

        .preset-name {
          font-size: 12px;
          color: var(--el-text-color-regular);
        }
      }
    }
  }

  .color-preview {
    .preview-title {
      margin: 0 0 12px 0;
      font-size: 14px;
      font-weight: 500;
      color: var(--el-text-color-primary);
    }

    .preview-content {
      .preview-buttons {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
        flex-wrap: wrap;
      }

      .gradient-preview {
        display: flex;
        align-items: center;
        gap: 8px;

        .gradient-bar {
          width: 100px;
          height: 20px;
          border-radius: 4px;
          border: 1px solid var(--el-border-color-light);
        }

        .gradient-label {
          font-size: 12px;
          color: var(--el-text-color-regular);
        }
      }
    }
  }
}
</style>