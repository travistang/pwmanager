<template>
  <mu-dialog
    :open="open"
    :title="isEdit?'Edit Password':'Add a Password'"
    @close="onClose"
  >
    <!-- left half-->
    <mu-flexbox>
      <mu-flexbox-item>
        <mu-content-block>
          <mu-text-field
            hintText="Password Name"
            v-model="passwordName"
            type="text"
            icon="contact_mail"
            :disabled="isEdit"
            :rowsMax="2"
            fullWidth
          />
          <br/>
          <mu-text-field
            hintText="Password"
            type="text"
            icon="vpn_key"
            v-model="passwordOrNull"
            :rowsMax="2"
            disabled
            fullWidth
          />
          <br/>
          <mu-flat-button
            label="Generate Password"
            class="demo-flat-button"
            :disabled="!isValidCriteria"
            @click="generatePassword"
            primary/>
        </mu-content-block>
      </mu-flexbox-item>
    <!-- right half -->
      <mu-flexbox-item>
        <mu-content-block>

          Password of {{passwordName}} contains:
          <div>
              <mu-chip
                v-for="(contain,cat) in passwordContains"
                @click="toggle(cat);"
                :backgroundColor="contain?'deepPurple400':'grey300'"
                :class="contain?'chip-selected':'chip'"

                >
                <mu-avatar :size="32">{{getAvatar(cat)}}</mu-avatar>
                {{catRepr(cat)}}
              </mu-chip>
          </div>
          <!-- <br/> -->
        </mu-content-block>
        <mu-content-block>
          Password Length: {{passwordLength}}
          <mu-slider v-model="passwordLength"
            :min="numCriteria || 1"
            :max="32"
            :step="1"
            :disabled="!isValidCriteria"
          />
        </mu-content-block>
      </mu-flexbox-item>
    </mu-flexbox>
    <mu-flat-button
      slot="actions"
      @click="onClose"
      secondary
      label="Cancel"
    />
    <mu-flat-button
      slot="actions"
      primary
      @click="onAction"
      :label="isEdit?'Update Password':'Create Password'"
      :disabled="!isValidCriteria"
    />
  </mu-dialog>
</template>

<script>
export default {
  props: {
    'password': {
      type: Object,
      // validator: function(pw)
      // {
      //   if (pw == null) return true
      //   return pw.name
      //       && pw.createdAt
      //       && pw.updatedAt
      //       && pw.password
      //       && pw.objectId
      // }
    },
    'isEdit':   Boolean,
    'open':     Boolean,
    'onClose':  Function,
    'onAction': Function,
  },
  data () {
    return {

      passwordContains: {
        number: true,
        lowercase: true,
        uppercase: true,
        symbols: true,
      },
      passwordLength: 8,
    }
  },
  watch: {
    passwordLength: function (res){this.generatePassword()},
    // address the problem that no password is given when a new password is created without clicking any buttons
    open: function(isOpened)
    {
      if(isOpened && this.password != null && this.password.password == '')
      {
         this.generatePassword();
      }
    },
    
  },

  computed: {
    isValidCriteria: function()
    {
      // check if all of the criteria has been disabled
      return Object.values(this.passwordContains)
          .reduce((p,q) => p || q)
    },
    numCriteria: function()
    {
      // get the number of criteria toggled on
      return Object.keys(this.passwordContains)
          .map((k) => this.passwordContains[k])
          .reduce((c,q) => q?(c + 1):c,0)
    },
    passwordName: {
      get: function()
      {
        return this.password?this.password.name:null
      },
      set: function(name)
      {
        if(this.password && !this.isEdit)
        {
          this.password.name = name
        }
      }
    },
    passwordOrNull: {
      get: function()
      {
        return this.password?this.password.password:null
      },
      set: function(password)
      {
        if(this.password)
        {
          this.password.password = password
        }
      }
    },
  },
  methods: {
    generatePassword: function()
    {
      if(!this.isValidCriteria)
        {
          this.password.password = ''
          return
        }
      // prepare functions
      const punc = "!@#$%^&*(){}:\"<>?\\\'/.,?><';[]|".split('')
      const alpha = "qwertyuiopasdfghjklzxcvbnm"
      const lower = alpha.split('')
      const upper = alpha.toUpperCase().split('')
      const nums = "1234567890".split('')

      // gather criteria
      let charPool = []
      let newPw = ''

      // and a helper function
      const draw = (list) => list[~~(Math.random() * list.length)]
      // start populating
      if(this.passwordContains.number){
        newPw += draw(nums)
        charPool = charPool.concat(nums)
      }
      if(this.passwordContains.lowercase){
        newPw += draw(lower)
        charPool = charPool.concat(lower)
      }
      if(this.passwordContains.uppercase){
        newPw += draw(upper)
        charPool = charPool.concat(upper)
      }
      if(this.passwordContains.symbols){
        newPw += draw(punc)
        charPool = charPool.concat(punc)
      }
      // and draw amoung the charPool...
      const charsRemain = this.passwordLength - newPw.length
      for(var i = 0; i < charsRemain; i++)
      {
          newPw += draw(charPool)
      }

      this.password.password = newPw

    },
    toggle: function(cat)
    {
      this.passwordContains[cat] = !this.passwordContains[cat]
      this.generatePassword()
    },
    catRepr: function(cat)
    {
      switch(cat)
      {
        case "number": return "Digits"
        case "lowercase": return "Lowercase"
        case "uppercase": return "Uppercase"
        default:
          return "Punctuations"
      }
    },
    getAvatar: function(cat)
    {
      switch(cat)
      {
        case "number": return "0"
        case "lowercase": return "a"
        case "uppercase": return "A"
        default:
          return "#"
      }
    },
  }
}
</script>
<style scoped>
.chip {
  margin: 4px;
  width: 45%;
}
.chip-selected{
  color: white;
  background-color:primary;
  margin:4px;
  width: 45%;
}
</style>
