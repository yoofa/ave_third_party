// Copyright 2022 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// This file was generated by:
//   tools/json_schema_compiler/compiler.py.
// NOTE: The format of types has changed. 'FooType' is now
//   'chrome.virtualKeyboardPrivate.FooType'.
// Please run the closure compiler before committing changes.
// See https://chromium.googlesource.com/chromium/src/+/main/docs/closure_compilation.md

/**
 * @fileoverview Externs generated from namespace: virtualKeyboardPrivate
 * @externs
 */

/** @const */
chrome.virtualKeyboardPrivate = {};

/**
 * @enum {string}
 */
chrome.virtualKeyboardPrivate.VirtualKeyboardEventType = {
  KEYUP: 'keyup',
  KEYDOWN: 'keydown',
};

/**
 * @typedef {{
 *   type: !chrome.virtualKeyboardPrivate.VirtualKeyboardEventType,
 *   charValue: number,
 *   keyCode: number,
 *   keyName: string,
 *   modifiers: (number|undefined)
 * }}
 */
chrome.virtualKeyboardPrivate.VirtualKeyboardEvent;

/**
 * @enum {string}
 */
chrome.virtualKeyboardPrivate.KeyboardMode = {
  FULL_WIDTH: 'FULL_WIDTH',
  FLOATING: 'FLOATING',
};

/**
 * @enum {string}
 */
chrome.virtualKeyboardPrivate.KeyboardState = {
  ENABLED: 'ENABLED',
  DISABLED: 'DISABLED',
  AUTO: 'AUTO',
};

/**
 * @typedef {{
 *   left: number,
 *   top: number,
 *   width: number,
 *   height: number
 * }}
 */
chrome.virtualKeyboardPrivate.Bounds;

/**
 * @typedef {{
 *   layout: string,
 *   hotrodmode: boolean,
 *   a11ymode: boolean,
 *   features: !Array<string>
 * }}
 */
chrome.virtualKeyboardPrivate.KeyboardConfig;

/**
 * @typedef {{
 *   mode: !chrome.virtualKeyboardPrivate.KeyboardMode,
 *   bounds: !chrome.virtualKeyboardPrivate.Bounds
 * }}
 */
chrome.virtualKeyboardPrivate.ContainerBehaviorOptions;

/**
 * @enum {string}
 */
chrome.virtualKeyboardPrivate.DisplayFormat = {
  TEXT: 'text',
  PNG: 'png',
  HTML: 'html',
  FILE: 'file',
};

/**
 * @typedef {{
 *   id: string,
 *   imageData: (string|undefined),
 *   textData: (string|undefined),
 *   displayFormat: !chrome.virtualKeyboardPrivate.DisplayFormat,
 *   timeCopied: number
 * }}
 */
chrome.virtualKeyboardPrivate.ClipboardItem;

/**
 * Inserts text into the currently focused text field.
 * @param {string} text The text that will be inserted.
 * @param {function(): void=} callback Called when the insertion is completed.
 */
chrome.virtualKeyboardPrivate.insertText = function(text, callback) {};

/**
 * Sends a fabricated key event to the focused input field.
 * @param {!chrome.virtualKeyboardPrivate.VirtualKeyboardEvent} keyEvent
 * @param {function(): void=} callback Called after processing the event.
 */
chrome.virtualKeyboardPrivate.sendKeyEvent = function(keyEvent, callback) {};

/**
 * Hides the virtual keyboard.
 * @param {function(): void=} callback Called when the keyboard is hidden.
 */
chrome.virtualKeyboardPrivate.hideKeyboard = function(callback) {};

/**
 * Sets the state of the hotrod virtual keyboard. This API should only be used
 * by hotrod.
 * @param {boolean} enable
 */
chrome.virtualKeyboardPrivate.setHotrodKeyboard = function(enable) {};

/**
 * Sets the lock state of the virtual keyboard. A locked keyboard remains
 * visible even after a text area loses input focus.
 * @param {boolean} lock
 */
chrome.virtualKeyboardPrivate.lockKeyboard = function(lock) {};

/**
 * Inform the system that the keyboard has loaded.
 * @param {function(): void=} callback Called when load acknowledgement is
 *     complete.
 */
chrome.virtualKeyboardPrivate.keyboardLoaded = function(callback) {};

/**
 * Gets the virtual keyboard configuration.
 * @param {function(!chrome.virtualKeyboardPrivate.KeyboardConfig): void}
 *     callback Called when querying virtual keyboard configuration is complete.
 */
chrome.virtualKeyboardPrivate.getKeyboardConfig = function(callback) {};

/**
 * Opens chrome://os-settings/osLanguages/input page.
 */
chrome.virtualKeyboardPrivate.openSettings = function() {};

/**
 * Opens chrome://os-settings/osLanguages/smartInputs page.
 */
chrome.virtualKeyboardPrivate.openSuggestionSettings = function() {};

/**
 * Sets the virtual keyboard container behavior
 * @param {!chrome.virtualKeyboardPrivate.ContainerBehaviorOptions} options
 *     Optional parameters for new container behavior.
 * @param {function(boolean): void=} callback Called when container mode is
 *     ready to change, or if the operation failed.
 */
chrome.virtualKeyboardPrivate.setContainerBehavior = function(options, callback) {};

/**
 * Sets the virtual keyboard draggable area bounds.
 * @param {!chrome.virtualKeyboardPrivate.Bounds} bounds The value of draggable
 *     rect area of floating keyboard.
 */
chrome.virtualKeyboardPrivate.setDraggableArea = function(bounds) {};

/**
 * Requests the virtual keyboard to change state.
 * @param {!chrome.virtualKeyboardPrivate.KeyboardState} state The value of the
 *     virtual keyboard state to change to.
 */
chrome.virtualKeyboardPrivate.setKeyboardState = function(state) {};

/**
 * Sets the areas on the screen that are blocked by the virtual keyboard.
 * @param {!Array<!chrome.virtualKeyboardPrivate.Bounds>} boundsList List of
 *     rectangles representing regions occluded by the keyboard.
 */
chrome.virtualKeyboardPrivate.setOccludedBounds = function(boundsList) {};

/**
 * Sets the areas on the keyboard window where events are handled. Any event
 * outside of these areas are passed on to the window behind it.
 * @param {!Array<!chrome.virtualKeyboardPrivate.Bounds>} boundsList List of
 *     rectangles representing regions where events targeting the keyboard
 *     should be handled.
 */
chrome.virtualKeyboardPrivate.setHitTestBounds = function(boundsList) {};

/**
 * Sets the area of the keyboard window that should not move off screen. Any
 * area outside of this can be moved off the user's screen.
 * @param {!chrome.virtualKeyboardPrivate.Bounds} bounds The bounds of the area
 *     inside the keyboard window, relative to the window origin, that should
 *     not be moved off screen. Any area outside of this bounds can be moved off
 *     screen.
 */
chrome.virtualKeyboardPrivate.setAreaToRemainOnScreen = function(bounds) {};

/**
 * Sets the bounds of the keyboard window in screen coordinates.
 * @param {!chrome.virtualKeyboardPrivate.Bounds} bounds A rectangle defining
 *     the new bounds of the window in screen coordinates.
 */
chrome.virtualKeyboardPrivate.setWindowBoundsInScreen = function(bounds) {};

/**
 * Get the clipboard history
 * @param {{
 *   itemIds: (!Array<string>|undefined)
 * }} options
 * @param {function(!Array<!chrome.virtualKeyboardPrivate.ClipboardItem>): void}
 *     callback Called when querying the ClipboardHistory is complete.
 */
chrome.virtualKeyboardPrivate.getClipboardHistory = function(options, callback) {};

/**
 * Pastes a clipboard item from the clipboard history.
 * @param {string} itemId The unique id which identifies this clipboard item.
 */
chrome.virtualKeyboardPrivate.pasteClipboardItem = function(itemId) {};

/**
 * Deletes a clipboard item from the clipboard history.
 * @param {string} itemId The unique id which identifies this clipboard item.
 */
chrome.virtualKeyboardPrivate.deleteClipboardItem = function(itemId) {};

/**
 * This event is sent when virtual keyboard bounds changed and overscroll/resize
 * is enabled.
 * @type {!ChromeEvent}
 */
chrome.virtualKeyboardPrivate.onBoundsChanged;

/**
 * Fired when the virtual keyboard window has been closed. For example, this can
 * happen when turning off on-screen keyboard or exiting tablet mode.
 * @type {!ChromeEvent}
 */
chrome.virtualKeyboardPrivate.onKeyboardClosed;

/**
 * Fired when a configuration for virtual keyboard IME has changed, e.g. auto
 * complete disabled.
 * @type {!ChromeEvent}
 */
chrome.virtualKeyboardPrivate.onKeyboardConfigChanged;

/**
 * Fired when the list of items in the clipboard history changes.
 * @type {!ChromeEvent}
 */
chrome.virtualKeyboardPrivate.onClipboardHistoryChanged;

/**
 * Fired when the data in a specific clipboard item is updated (mainly used for
 * sending updated rendered html image).
 * @type {!ChromeEvent}
 */
chrome.virtualKeyboardPrivate.onClipboardItemUpdated;

/**
 * Fired when the color provider of virtual keyboard window has changed.
 * @type {!ChromeEvent}
 */
chrome.virtualKeyboardPrivate.onColorProviderChanged;
